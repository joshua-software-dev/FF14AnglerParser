#! /usr/bin/env python3

import asyncio
import os

from ff14angler.constants.values import EXPORT_DIRECTORY
from ff14angler.dataClasses.cache.xivapiCache import XivapiCache
from ff14angler.scraper.scraper import Scraper
from ff14angler.network.chromeWrapper import ChromeWrapper
from ff14angler.network.xivapiWrapper import XivapiWrapper


def main():
    cache_path = os.path.join(EXPORT_DIRECTORY, 'xivapi_cache.json')

    try:
        with open(cache_path) as fh:
            print('Reading API cache into memory...')
            XivapiWrapper.cache = XivapiCache.from_json(fh.read())
    except FileNotFoundError:
        print('No API cache found.')

    try:
        print('Starting Chrome...')
        with ChromeWrapper(headless=True) as driver:
            print('Beginning scraping...')
            loop = asyncio.get_event_loop()
            loop.run_until_complete(Scraper.main(driver))
    finally:
        print('Writing API cache to disk...')
        with open(cache_path, 'w+') as fh:
            fh.write(XivapiWrapper.cache.to_json())
