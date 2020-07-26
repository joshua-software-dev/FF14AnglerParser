#! /usr/bin/env python3

import os

from pprint import pprint

from selenium.webdriver.chrome.webdriver import WebDriver

from .fishPage import FishPage
from .homePage import HomePage


class Fetch:

    @staticmethod
    async def main(driver: WebDriver):
        os.makedirs('angler', exist_ok=True)
        homepage_data = await HomePage.collect_homepage_data(driver)
        fish_data_list = await FishPage.collect_fish_data(driver, homepage_data['fish'])

        pprint(homepage_data)
        pprint(fish_data_list)
