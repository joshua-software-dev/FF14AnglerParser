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
from ff14angler.dataClasses.comment.commentSection import CommentSection
from ff14angler.dataClasses.spot.spotProvider import SpotProvider
from ff14angler.network.delayOnReleaseLock import DelayOnReleaseLock


class SpotPage:

    @classmethod
    async def collect_spot_data(cls, driver: WebDriver):
        spot_url_template = urllib.parse.urljoin(ANGLER_BASE_URL, '/spot/')
        lock = DelayOnReleaseLock(ANGLER_DELAY_BETWEEN_REQUESTS_DURATION)

        for spot_id, spot in SpotProvider.spot_holder.items():
            angler_url: str = urllib.parse.urljoin(spot_url_template, str(spot_id))
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

                        await spot.update_spot_with_comment_section(
                            await CommentSection.get_comment_section_from_web_driver(driver)
                        )
                    break
                except (TimeoutException, ValueError):
                    if attempt == 2:
                        raise

            await spot.update_spot_with_spot_soup(BeautifulSoup(html, lxml.__name__))
