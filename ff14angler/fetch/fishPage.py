#! /usr/bin/env python3

import time

import lxml

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from ff14angler.dataClasses.fish.fishProvider import FishProvider


class FishPage:

    # noinspection SpellCheckingInspection
    @staticmethod
    async def load_all_comments_on_fish_page(driver: WebDriver):
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

    @classmethod
    async def collect_fish_data(cls, driver: WebDriver):
        fish_url_template = 'https://en.ff14angler.com/fish/{}'

        for fish_id, fish in FishProvider.fish_holder.items():
            angler_url: str = fish_url_template.format(fish_id)
            print(f'Scraping page: {angler_url}')
            driver.get(angler_url)

            try:
                WebDriverWait(driver, 60).until(
                    expected_conditions.presence_of_element_located(
                        (By.CSS_SELECTOR, 'form.comment_form')
                    )
                )
            except TimeoutException:
                raise

            await cls.load_all_comments_on_fish_page(driver)
            await fish.update_fish_with_fish_soup(BeautifulSoup(driver.page_source, lxml.__name__))
