#! /usr/bin/env python3

import aiohttp

from asyncio_throttle import Throttler


class AiohttpWrapper:

    def __init__(self, rate_limit: int, duration: int):
        """The value `rate_limit` is max requests per duration. Duration is integer value in seconds."""
        self._throttler = Throttler(rate_limit=rate_limit, period=duration)

    async def get_json_at_url(self, url: str):
        async with self._throttler:
            async with aiohttp.ClientSession() as session:
                print(f'Fetching URL: {url}')
                async with session.get(url) as response:
                    return await response.json()

    async def get_text_at_url(self, url: str) -> str:
        async with self._throttler:
            async with aiohttp.ClientSession() as session:
                print(f'Fetching URL: {url}')
                async with session.get(url) as response:
                    return await response.text()
