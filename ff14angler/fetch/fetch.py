#! /usr/bin/env python3

import json
import os

from selenium.webdriver.chrome.webdriver import WebDriver  # type: ignore

from ff14angler.constants.values import EXPORT_DIRECTORY
from ff14angler.export.dunderSerializer import DunderSerializer
from ff14angler.export.tableExport import TableExport
from ff14angler.fetch.baitPage import BaitPage
from ff14angler.fetch.fishPage import FishPage
from ff14angler.fetch.homePage import HomePage
from ff14angler.fetch.spotPage import SpotPage


class Fetch:

    @staticmethod
    async def main(driver: WebDriver):
        scraping_data = await HomePage.collect_homepage_data(driver)

        await BaitPage.collect_bait_data(driver)
        await FishPage.collect_fish_data(driver)
        await SpotPage.collect_spot_data(driver)

        print('Writing JSON dump form scraping results...')
        os.makedirs(EXPORT_DIRECTORY, exist_ok=True)
        with open(os.path.join(EXPORT_DIRECTORY, 'full_dump.json'), 'w+') as fh:
            json.dump(scraping_data, fh, cls=DunderSerializer, indent=4, sort_keys=True)

        print('Writing table form scraping results...')
        os.makedirs(os.path.join(EXPORT_DIRECTORY, 'table_data'), exist_ok=True)
        await TableExport.output_data_for_database(scraping_data)

        print('Writing bait one entry per file scraping results...')
        bait_dir = os.path.join(EXPORT_DIRECTORY, 'bait_data')
        os.makedirs(bait_dir, exist_ok=True)
        for angler_bait_id, bait_data in scraping_data.bait.items():
            with open(os.path.join(bait_dir, f'{angler_bait_id}.json'), 'w+') as fh:
                json.dump(bait_data, fh, cls=DunderSerializer, indent=4, sort_keys=True)

        print('Writing fish one entry per file scraping results...')
        fish_dir = os.path.join(EXPORT_DIRECTORY, 'fish_data')
        os.makedirs(fish_dir, exist_ok=True)
        for angler_fish_id, fish_data in scraping_data.fish.items():
            with open(os.path.join(fish_dir, f'{angler_fish_id}.json'), 'w+') as fh:
                json.dump(fish_data, fh, cls=DunderSerializer, indent=4, sort_keys=True)

        print('Writing spot one entry per file scraping results...')
        spot_dir = os.path.join(EXPORT_DIRECTORY, 'spot_data')
        os.makedirs(spot_dir, exist_ok=True)
        for angler_spot_id, spot_data in scraping_data.spot.items():
            with open(os.path.join(spot_dir, f'{angler_spot_id}.json'), 'w+') as fh:
                json.dump(spot_data, fh, cls=DunderSerializer, indent=4, sort_keys=True)
