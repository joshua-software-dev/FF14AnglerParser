#! /usr/bin/env python3

import asyncio

from .chromeWrapper import ChromeWrapper
from .fetch.fetch import Fetch


with ChromeWrapper() as driver:
    asyncio.run(Fetch.main(driver))
