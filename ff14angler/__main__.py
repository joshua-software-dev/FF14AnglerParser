#! /usr/bin/env python3

import asyncio
import pickle

from ff14angler.network.chromeWrapper import ChromeWrapper
from ff14angler.fetch.fetch import Fetch
from ff14angler.xivapi import XivApi


def main():
    try:
        with open('data/xivapi_cache.pickle', 'rb') as fh:
            print('Reading API cache into memory...')
            XivApi.cached_responses.update(pickle.load(fh))
    except FileNotFoundError:
        print('No API cache found.')

    try:
        print('Starting Chrome...')
        with ChromeWrapper() as driver:
            print('Beginning scraping...')
            loop = asyncio.get_event_loop()
            loop.run_until_complete(Fetch.main(driver))
    finally:
        print('Writing binary API cache to disk...')
        with open('data/xivapi_cache.pickle', 'wb+') as fh:
            pickle.dump(XivApi.cached_responses, fh)
