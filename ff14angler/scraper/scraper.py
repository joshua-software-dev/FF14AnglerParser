#! /usr/bin/env python3

import json
import os

from selenium.webdriver.chrome.webdriver import WebDriver  # type: ignore

from ff14angler.constants.values import EXPORT_DIRECTORY
from ff14angler.database.sqliteExport import SQLiteExport
from ff14angler.scraper.baitScraper import BaitScraper
from ff14angler.scraper.fishScraper import FishScraper
from ff14angler.scraper.homePageScraper import HomePageScraper
from ff14angler.scraper.spotScraper import SpotScraper


class Scraper:

    @staticmethod
    async def main(driver: WebDriver):
        scraping_data = await HomePageScraper.collect_homepage_data(driver)

        await BaitScraper.collect_bait_data(driver)
        await FishScraper.collect_fish_data(driver)
        await BaitScraper.update_all_bait_mooch_fish_with_large_icon_url()
        await SpotScraper.collect_spot_data(driver)

        print('Writing JSON dump form scraping results...')
        os.makedirs(EXPORT_DIRECTORY, exist_ok=True)
        with open(os.path.join(EXPORT_DIRECTORY, 'full_dump.json'), 'w+') as fh:
            json.dump(scraping_data.to_dict(), fh, indent=4, sort_keys=True)

        print('Writing database form scraping results...')
        SQLiteExport.output_data_as_database(scraping_data)
