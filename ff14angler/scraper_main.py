#! /usr/bin/env python3

import argparse
import asyncio
import os

from ff14angler.constants.values import config_settings
from ff14angler.dataClasses.cache.xivapiCache import XivapiCache
from ff14angler.scraper.scraper import Scraper
from ff14angler.network.chromeWrapper import ChromeWrapper
from ff14angler.network.xivapiWrapper import XivapiWrapper


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-e',
        '--export-directory',
        action='store',
        dest='export_directory',
        default=None,
        help='Directory to place API cache, and game icon images.'
    )
    config_settings['EXPORT_DIRECTORY'] = (
        arg_parser.parse_args().export_directory or config_settings['EXPORT_DIRECTORY']
    )

    cache_path = os.path.join(config_settings['EXPORT_DIRECTORY'], 'xivapi_cache.json')

    try:
        with open(cache_path) as fh:
            print('Reading API cache into memory...')
            XivapiWrapper.cache = XivapiCache.from_json(fh.read())
    except FileNotFoundError:
        print('No API cache found.')

    try:
        print('Starting Chrome...')
        with ChromeWrapper() as driver:
            print('Beginning scraping...')
            loop = asyncio.get_event_loop()
            loop.run_until_complete(Scraper.main(driver))
    finally:
        print('Writing API cache to disk...')
        with open(cache_path, 'w+') as fh:
            fh.write(XivapiWrapper.cache.to_json())
