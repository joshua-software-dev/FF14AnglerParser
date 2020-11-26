#! /usr/bin/env python3

import asyncio
import urllib.parse

import lxml  # type: ignore

from bs4 import BeautifulSoup  # type: ignore
from selenium.common.exceptions import TimeoutException  # type: ignore
from selenium.webdriver.chrome.webdriver import WebDriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions  # type: ignore

from ff14angler.constants.values import (
    ANGLER_BASE_URL,
    ANGLER_PAGE_LOAD_WAIT_DURATION,
    ANGLER_DELAY_BETWEEN_REQUESTS_DURATION
)
from ff14angler.dataClasses.bait.bait import Bait
from ff14angler.dataClasses.bait.baitProvider import BaitProvider
from ff14angler.dataClasses.comment.commentSection import CommentSection
from ff14angler.exceptions.networkException import NetworkException
from ff14angler.scraper.lodestoneImageScraper import LodestoneImageScraper
from ff14angler.network.delayOnReleaseLock import DelayOnReleaseLock


class BaitScraper:

    @staticmethod
    async def update_bait_with_large_icon_url(bait: Bait, driver: WebDriver):
        if bait.bait_angler_lodestone_url:
            if bait.bait_icon_url is None:
                raise ValueError(f'Missing icon url from xivapi: {bait}')

            bait.bait_large_icon_url = await LodestoneImageScraper.get_large_icon(
                driver=driver,
                short_icon_url=bait.bait_icon_url,
                lodestone_url=bait.bait_angler_lodestone_url
            )

    @staticmethod
    async def ensure_all_bait_mooch_fish_up_to_date():
        for bait_id, bait in BaitProvider.bait_holder.items():
            if bait.bait_angler_is_mooch_fish:
                await bait.update_bait_with_assume_is_mooch_fish(False)

    @classmethod
    async def collect_bait_data(cls, driver: WebDriver):
        bait_url_template = urllib.parse.urljoin(ANGLER_BASE_URL, '/bait/')
        lock = DelayOnReleaseLock(ANGLER_DELAY_BETWEEN_REQUESTS_DURATION)

        for bait_id, bait in BaitProvider.bait_holder.items():
            angler_url: str = urllib.parse.urljoin(bait_url_template, str(bait_id))
            for attempt in range(3):
                driver.get('about:blank')
                print(f'Scraping page: {angler_url}')
                driver.get(angler_url)

                try:
                    WebDriverWait(driver, ANGLER_PAGE_LOAD_WAIT_DURATION).until(
                        expected_conditions.presence_of_element_located(
                            (By.CSS_SELECTOR, 'form.comment_form')
                        )
                    )

                    async with lock:
                        await asyncio.sleep(2)
                        html: str = driver.page_source

                        await bait.update_bait_with_comment_section(
                            await CommentSection.get_comment_section_from_web_driver(driver)
                        )
                    break
                except (NetworkException, TimeoutException, ValueError,):
                    if attempt == 2:
                        raise

            await bait.update_bait_with_bait_soup(BeautifulSoup(html, lxml.__name__))
            await cls.update_bait_with_large_icon_url(bait, driver)
