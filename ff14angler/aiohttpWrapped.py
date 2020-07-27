#! /usr/bin/env python3

import urllib.parse

import aiohttp

from asyncio_throttle import Throttler


# noinspection SpellCheckingInspection
class AiohttpWrapped:
    _throttler = Throttler(
        rate_limit=10,
        period=3  # seconds
    )

    @classmethod
    async def get_json_at_url(cls, url: str):
        async with cls._throttler:
            async with aiohttp.ClientSession() as session:  # type: aiohttp.ClientSession
                async with session.get(url) as response:  # type: aiohttp.ClientResponse
                    return await response.json()

    @classmethod
    async def get_text_at_url(cls, url: str) -> str:
        async with cls._throttler:
            async with aiohttp.ClientSession() as session:  # type: aiohttp.ClientSession
                async with session.get(url) as response:  # type: aiohttp.ClientResponse
                    return await response.text()

    @classmethod
    async def xivapi_fishing_spot_lookup(cls, fishing_spot_id: int):
        return await cls.get_json_at_url(f'https://xivapi.com/FishingSpot/{fishing_spot_id}')

    @classmethod
    async def xivapi_item_lookup(cls, item_id: int):
        return await cls.get_json_at_url(f'https://xivapi.com/Item/{item_id}')

    @classmethod
    async def xivapi_item_search(cls, item_name: str):
        return await cls.get_json_at_url(
            f'https://xivapi.com/search?indexes=Item&string={urllib.parse.quote(item_name)}'
        )

    @classmethod
    async def xivapi_place_name_lookup(cls, place_id: int):
        return await cls.get_json_at_url(f'https://xivapi.com/PlaceName/{place_id}')

    @classmethod
    async def xivapi_place_name_search(cls, place_name: str):
        return await cls.get_json_at_url(
            f'https://xivapi.com/search?indexes=PlaceName&string={urllib.parse.quote(place_name)}'
        )
