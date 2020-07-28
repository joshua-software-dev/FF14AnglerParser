#! /usr/bin/env python3

import json
import os

from selenium.webdriver.chrome.webdriver import WebDriver

from .fishPage import FishPage, FishProvider
from .homePage import HomePage
from ..dunderSerializer import DunderSerializer


class Fetch:

    @staticmethod
    async def main(driver: WebDriver):
        homepage_data = await HomePage.collect_homepage_data(driver)
        os.makedirs('data', exist_ok=True)
        # quick write to prevent losing data in event of crash
        with open('data/home_page.json', 'w+') as fh:
            json.dump(homepage_data, fh, cls=DunderSerializer, indent=4)

        await FishPage.collect_fish_data(driver)
        os.makedirs('data/fish_data', exist_ok=True)
        for fish_data in FishProvider.fish_holder.values():
            with open(f'data/fish_data/{fish_data.fish_data_angler_fish_id}.json', 'w+') as fh:
                json.dump(fish_data, fh, cls=DunderSerializer, indent=4, sort_keys=True)

        # Write again with updates to bait data
        with open('data/home_page.json', 'w+') as fh:
            json.dump(homepage_data, fh, cls=DunderSerializer, indent=4, sort_keys=True)
