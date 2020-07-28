#! /usr/bin/env python3

import asyncio
import json

import umsgpack

from .chromeWrapper import ChromeWrapper
from .fetch.fetch import Fetch
from .xivapi import XivApi


def main():
    try:
        with open('data/xivapi_cache.bin', 'rb') as fh:
            print('Reading API cache into memory...')
            XivApi.cached_responses.update(umsgpack.load(fh))
    except FileNotFoundError:
        print('No API cache found.')
        pass

    try:
        print('Starting Chrome...')
        with ChromeWrapper() as driver:
            print('Beginning scraping...')
            asyncio.run(Fetch.main(driver))
    finally:
        print('Writing binary API cache to disk...')
        with open('data/xivapi_cache.bin', 'wb+') as fh:
            umsgpack.dump(XivApi.cached_responses, fh)

        print('Writing text API cache to disk...')
        with open('data/xivapi_cache.json', 'w+') as fh:
            json.dump(XivApi.cached_responses, fh, indent=4)
