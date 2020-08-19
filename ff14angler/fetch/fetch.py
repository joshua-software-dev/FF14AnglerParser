#! /usr/bin/env python3

import json
import os

from selenium.webdriver.chrome.webdriver import WebDriver  # type: ignore

from ff14angler.constants.values import EXPORT_DIRECTORY
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
            json.dump(scraping_data.to_dict(), fh, indent=4, sort_keys=True)

        print('Writing table form scraping results...')
        await TableExport.output_data_for_database(scraping_data)
