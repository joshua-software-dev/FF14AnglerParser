#! /usr/bin/env python3

import asyncio

from ff14angler.dataClasses.cache.xivapiCache import XivapiCache
from ff14angler.network.chromeWrapper import ChromeWrapper
from ff14angler.network.xivapiWrapper import XivapiWrapper
from ff14angler.fetch.fetch import Fetch


def main():
    try:
        with open('data/xivapi_cache.json') as fh:
            print('Reading API cache into memory...')
            XivapiWrapper.cache = XivapiCache.from_json(fh.read())
    except FileNotFoundError:
        print('No API cache found.')

    try:
        print('Starting Chrome...')
        with ChromeWrapper() as driver:
            print('Beginning scraping...')
            loop = asyncio.get_event_loop()
            loop.run_until_complete(Fetch.main(driver))
    finally:
        print('Writing API cache to disk...')
        with open('data/xivapi_cache.json', 'w+') as fh:
            fh.write(XivapiWrapper.cache.to_json())
