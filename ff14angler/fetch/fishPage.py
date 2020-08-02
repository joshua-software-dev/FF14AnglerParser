#! /usr/bin/env python3

import asyncio
import urllib.parse

import lxml

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from ff14angler.constants.values import (
    ANGLER_BASE_URL,
    ANGLER_PAGE_LOAD_WAIT_DURATION,
    ANGLER_DELAY_BETWEEN_REQUESTS_DURATION
)
from ff14angler.dataClasses.comment.commentSection import CommentSection
from ff14angler.dataClasses.fish.fishProvider import FishProvider
from ff14angler.network.delayOnReleaseLock import DelayOnReleaseLock


class FishPage:

    @classmethod
    async def collect_fish_data(cls, driver: WebDriver):
        fish_url_template = urllib.parse.urljoin(ANGLER_BASE_URL, '/fish/')
        lock = DelayOnReleaseLock(ANGLER_DELAY_BETWEEN_REQUESTS_DURATION)

        for fish_id, fish in FishProvider.fish_holder.items():
            angler_url: str = urllib.parse.urljoin(fish_url_template, str(fish_id))
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

                        await fish.update_fish_with_comment_section(
                            await CommentSection.get_comment_section_from_web_driver(driver)
                        )
                    break
                except (TimeoutException, ValueError):
                    if attempt == 2:
                        raise

            await fish.update_fish_with_fish_soup(BeautifulSoup(html, lxml.__name__))
