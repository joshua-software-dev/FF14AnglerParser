#! /usr/bin/env python3

import lxml

from typing import Dict, List

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from ..dataClasses.fishData import FishData


class FishPage:

    @staticmethod
    async def parse_fish_data(html: str) -> FishData:
        return FishData.get_fish_data_from_soup(BeautifulSoup(html, lxml.__name__))

    @classmethod
    async def collect_fish_data(cls, driver: WebDriver, fish_list: Dict[int, str]) -> List[FishData]:
        fish_url_template = 'https://en.ff14angler.com/fish/{}'
        # temp overwrite to avoid spamming website before scraper is finished.
        fish_list = {1: 'Malm Kelp'}  # TODO: Remove

        temp_fish_data_list: List[FishData] = []

        for fish_id, fish_name in fish_list.items():
            driver.get(fish_url_template.format(fish_id))

            try:
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.CLASS_NAME, 'fish_info')
                    )
                )
            except TimeoutException:
                raise

            fish_data = await cls.parse_fish_data(driver.page_source)
            temp_fish_data_list.append(fish_data)

        return temp_fish_data_list
