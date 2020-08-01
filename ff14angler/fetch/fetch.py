#! /usr/bin/env python3

import json
import os

from selenium.webdriver.chrome.webdriver import WebDriver

from ff14angler.dunderSerializer import DunderSerializer
from ff14angler.fetch.baitPage import BaitPage
from ff14angler.fetch.fishPage import FishPage
from ff14angler.fetch.homePage import HomePage
from ff14angler.fetch.spotPage import SpotPage


class Fetch:

    @staticmethod
    async def main(driver: WebDriver):
        homepage_data = await HomePage.collect_homepage_data(driver)

        os.makedirs('data', exist_ok=True)
        with open('data/home_page.json', 'w+') as fh:
            json.dump(homepage_data, fh, cls=DunderSerializer, indent=4, sort_keys=True)

        await BaitPage.collect_bait_data(driver)
        await FishPage.collect_fish_data(driver)
        await SpotPage.collect_spot_data(driver)

        print('Writing LARGE scraping results...')
        os.makedirs('data', exist_ok=True)
        with open('data/home_page.json', 'w+') as fh:
            json.dump(homepage_data, fh, cls=DunderSerializer, indent=4, sort_keys=True)

        print('Writing bait page scraping results...')
        os.makedirs('data/bait_data', exist_ok=True)
        for angler_bait_id, bait_data in homepage_data['bait'].items():  # type: int, 'Any'
            with open(f'data/bait_data/{angler_bait_id}.json', 'w+') as fh:
                json.dump(bait_data, fh, cls=DunderSerializer, indent=4, sort_keys=True)

        print('Writing fish page scraping results...')
        os.makedirs('data/fish_data', exist_ok=True)
        for angler_fish_id, fish_data in homepage_data['fish'].items():  # type: int, 'Any'
            with open(f'data/fish_data/{angler_fish_id}.json', 'w+') as fh:
                json.dump(fish_data, fh, cls=DunderSerializer, indent=4, sort_keys=True)

        print('Writing spot page scraping results...')
        os.makedirs('data/spot_data', exist_ok=True)
        for angler_spot_id, spot_data in homepage_data['spot'].items():  # type: int, 'Any'
            with open(f'data/spot_data/{angler_spot_id}.json', 'w+') as fh:
                json.dump(spot_data, fh, cls=DunderSerializer, indent=4, sort_keys=True)
