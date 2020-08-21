#! /usr/bin/env python3

import aiohttp

from typing import Any, Dict

from asyncio_throttle import Throttler

from ff14angler.exceptions.networkException import NetworkException


class AiohttpWrapper:

    def __init__(self, rate_limit: int, duration: int):
        """The value `rate_limit` is max requests per duration. Duration is integer value in seconds."""
        self._throttler = Throttler(rate_limit=rate_limit, period=duration)

    async def get_bytes_at_url(self, url: str) -> bytes:
        async with self._throttler:
            try:
                async with aiohttp.ClientSession() as session:
                    print(f'Downloading URL: {url}')
                    async with session.get(url) as response:
                        return await response.read()
            except aiohttp.ClientError as e:
                raise NetworkException(e)

    async def get_json_at_url(self, url: str) -> Dict[str, Any]:
        async with self._throttler:
            try:
                async with aiohttp.ClientSession() as session:
                    print(f'Fetching URL: {url}')
                    async with session.get(url) as response:
                        return await response.json()
            except aiohttp.ClientError as e:
                raise NetworkException(e)

    async def get_text_at_url(self, url: str) -> str:
        async with self._throttler:
            try:
                async with aiohttp.ClientSession() as session:
                    print(f'Fetching URL: {url}')
                    async with session.get(url) as response:
                        return await response.text()
            except aiohttp.ClientError as e:
                raise NetworkException(e)

    async def post_json_at_url(self, url: str, item_name: str, json_obj: Dict[str, Any]) -> Dict[str, Any]:
        async with self._throttler:
            try:
                async with aiohttp.ClientSession() as session:
                    print(f'Fetching URL: {url} : {item_name}')
                    async with session.post(url, json=json_obj) as response:
                        return await response.json()
            except aiohttp.ClientError as e:
                raise NetworkException(e)
