#! /usr/bin/env python3

import json
import os

from selenium.webdriver.chrome.webdriver import WebDriver

from .fishPage import FishPage
from .homePage import HomePage
from ..dunderSerializer import DunderSerializer


class Fetch:

    @staticmethod
    async def main(driver: WebDriver):
        os.makedirs('angler', exist_ok=True)
        homepage_data = await HomePage.collect_homepage_data(driver)
        fish_data_list = await FishPage.collect_fish_data(driver, homepage_data['fish'])

        print(json.dumps(homepage_data, cls=DunderSerializer, indent=4))
        print(json.dumps(fish_data_list, cls=DunderSerializer, indent=4))
