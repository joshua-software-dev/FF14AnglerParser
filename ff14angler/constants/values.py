#! /usr/bin/env python3

import os


ANGLER_API_BASE_URL = 'https://angler.heliohost.org/'
ANGLER_BASE_URL = 'https://en.ff14angler.com'
# Integer number of seconds
ANGLER_DELAY_BETWEEN_REQUESTS_DURATION = 3
# Integer number of seconds
ANGLER_PAGE_LOAD_WAIT_DURATION = 180
ANGLER_SPEARFISHING_BAIT_ITEM_ID = 17726  # Spearfishing Gig Offhand Item
ANGLER_SPEARFISHING_BAIT_ITEM_LEVEL = 61
DEBUG_SERVER = False
MODULE_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
EXPORT_DIRECTORY = os.path.join(os.path.abspath(os.path.join(MODULE_DIRECTORY, '..')), 'static')
SQLITE_DIRECTORY = os.path.join(MODULE_DIRECTORY, 'sqlite_db')
SQLITE_DATABASE = os.path.join(SQLITE_DIRECTORY, 'angler_api.db')
XIVAPI_BASE_URL = 'https://xivapi.com'
