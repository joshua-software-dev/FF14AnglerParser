#! /usr/bin/env python3

import time

import lxml

from typing import Dict, List

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from ..dataClasses.fishData import FishData


class FishPage:

    # noinspection SpellCheckingInspection
    @staticmethod
    async def load_all_comments(driver: WebDriver):
        form = driver.find_element_by_css_selector('form.comment_form')
        ActionChains(driver).move_to_element(form).perform()

        try:
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.comment')
                )
            )
        except TimeoutException:
            return

        while True:
            try:
                WebDriverWait(driver, 3).until(
                    expected_conditions.presence_of_element_located(
                        (By.CSS_SELECTOR, 'div.comment_continue a')
                    )
                )
            except TimeoutException:
                return

            try:
                comment_continue = driver.find_element_by_css_selector('div.comment_continue a')
                comment_continue.click()
                ActionChains(driver).move_to_element(form).perform()
                time.sleep(1)
            except (NoSuchElementException, StaleElementReferenceException):
                print('WARNING: Failed to click load more comments after element was found successfully.')

    @staticmethod
    async def parse_fish_data(html: str) -> FishData:
        return await FishData.get_fish_data_from_soup(BeautifulSoup(html, lxml.__name__))

    @classmethod
    async def collect_fish_data(cls, driver: WebDriver, fish_list: Dict[int, str]) -> List[FishData]:
        fish_url_template = 'https://en.ff14angler.com/fish/{}'
        # temp overwrite to avoid spamming website before scraper is finished.
        fish_list = {1: 'Malm Kelp', 2: 'Crayfish'}  # TODO: Remove

        temp_fish_data_list: List[FishData] = []

        for fish_id, fish_name in fish_list.items():
            driver.get(fish_url_template.format(fish_id))

            try:
                WebDriverWait(driver, 60).until(
                    expected_conditions.presence_of_element_located(
                        (By.CSS_SELECTOR, 'form.comment_form')
                    )
                )
            except TimeoutException:
                raise

            await cls.load_all_comments(driver)
            fish_data = await cls.parse_fish_data(driver.page_source)
            temp_fish_data_list.append(fish_data)

        return temp_fish_data_list
