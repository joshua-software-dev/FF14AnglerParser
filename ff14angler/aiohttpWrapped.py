#! /usr/bin/env python3

import asyncio
import urllib.parse

import aiohttp

from typing import List, Set, Tuple

from asyncio_throttle import Throttler

from ff14angler.xivapi import XivApi


# noinspection SpellCheckingInspection
class AiohttpWrapped:
    _throttler = Throttler(
        rate_limit=3,
        period=3  # seconds
    )

    @classmethod
    async def get_json_at_url(cls, url: str):
        async with cls._throttler:
            async with aiohttp.ClientSession() as session:
                print(f'Fetching URL: {url}')
                async with session.get(url) as response:
                    return await response.json()

    @classmethod
    async def get_text_at_url(cls, url: str) -> str:
        async with cls._throttler:
            async with aiohttp.ClientSession() as session:
                print(f'Fetching URL: {url}')
                async with session.get(url) as response:
                    return await response.text()

    @classmethod
    async def xivapi_fish_parameter_lookup(cls, fish_param_id: int):
        if result := XivApi.cached_responses['FishParameter'].get(fish_param_id):
            return result

        data = await cls.get_json_at_url(f'https://xivapi.com/FishParameter/{fish_param_id}')
        XivApi.cached_responses['FishParameter'][fish_param_id] = data
        return data

    @classmethod
    async def xivapi_fishing_spot_lookup(cls, fishing_spot_id: int):
        if result := XivApi.cached_responses['FishingSpot'].get(fishing_spot_id):
            return result

        data = await cls.get_json_at_url(f'https://xivapi.com/FishingSpot/{fishing_spot_id}')
        XivApi.cached_responses['FishingSpot'][fishing_spot_id] = data
        return data

    @classmethod
    async def xivapi_gathering_point_base_index(cls):
        if result := XivApi.cached_responses['Search']['GatheringPointBase'].get('search'):
            return result

        temp_results = []
        page_num: int = 1

        while True:
            response = await cls.get_json_at_url(f'https://xivapi.com/GatheringPointBase?limit=1000&page={page_num}')
            page_num: int = response['Pagination']['Page']
            max_pages: int = response['Pagination']['PageTotal']
            temp_results += response['Results']

            if page_num >= max_pages:
                XivApi.cached_responses['Search']['GatheringPointBase']['search'] = temp_results
                return temp_results

            page_num += 1

    @classmethod
    async def xivapi_spearfishing_gathering_point_base_index(cls):
        if result := XivApi.cached_responses['Search']['GatheringPointBase'].get('spear'):
            return result

        gathering_point_base_spearfishing_spots: List[Tuple[Set[int], int, int]] = []
        index_response = await cls.xivapi_gathering_point_base_index()
        index_lookup = await asyncio.gather(
            *(cls.xivapi_gathering_point_base_lookup(gpb['ID']) for gpb in index_response)
        )

        for gpb_result in index_lookup:
            try:
                gpb_result['GatheringTypeTargetID']
            except KeyError:
                print(gpb_result)
                raise

            if gpb_result['GatheringTypeTargetID'] == 4:
                spearfishing_ids: Set[int] = set()
                for i in range(8):
                    if (key := gpb_result.get(f'Item{i}')) not in [0, None]:
                        spearfishing_ids.add(key)

                if spearfishing_ids:
                    gathering_point_base_spearfishing_spots.append(
                        (
                            spearfishing_ids,
                            gpb_result['ID'],
                            gpb_result['GatheringLevel'],
                        )
                    )

        XivApi.cached_responses['Search']['GatheringPointBase']['spear'] = gathering_point_base_spearfishing_spots
        return gathering_point_base_spearfishing_spots

    @classmethod
    async def xivapi_gathering_point_base_lookup(cls, gathering_point_base_id: int):
        if result := XivApi.cached_responses['GatheringPointBase'].get(gathering_point_base_id):
            return result

        data = await cls.get_json_at_url(f'https://xivapi.com/GatheringPointBase/{gathering_point_base_id}')
        XivApi.cached_responses['GatheringPointBase'][gathering_point_base_id] = data
        return data

    @classmethod
    async def xivapi_item_lookup(cls, item_id: int):
        if result := XivApi.cached_responses['Item'].get(item_id):
            return result

        data = await cls.get_json_at_url(f'https://xivapi.com/Item/{item_id}')
        XivApi.cached_responses['Item'][item_id] = data
        return data

    @classmethod
    async def _xivapi_item_search(cls, item_name: str, page_num: int):
        return await cls.get_json_at_url(
            f'https://xivapi.com/search?indexes=Item&page={page_num}&string={urllib.parse.quote(item_name)}'
        )

    @classmethod
    async def xivapi_item_search(cls, item_name: str):
        if result := XivApi.cached_responses['Search']['Item'].get(item_name):
            return result

        page_num: int = 1
        max_pages: int = 99
        while page_num <= max_pages:
            response = await cls._xivapi_item_search(item_name, page_num)
            page_num = response['Pagination']['Page']
            max_pages = response['Pagination']['PageTotal']

            for result in response['Results']:
                if result['Name'].casefold() == item_name.casefold():
                    XivApi.cached_responses['Search']['Item'][item_name] = result
                    return result

            page_num += 1

        raise ValueError(f'Could not find applicable result for search term: {item_name}')

    @classmethod
    async def xivapi_leve_lookup(cls, leve_id: int):
        if result := XivApi.cached_responses['Leve'].get(leve_id):
            return result

        data = await cls.get_json_at_url(f'https://xivapi.com/Leve/{leve_id}')
        XivApi.cached_responses['Leve'][leve_id] = data
        return data

    @classmethod
    async def _xivapi_leve_search(cls, leve_name: str, page_num: int):
        return await cls.get_json_at_url(
            f'https://xivapi.com/search?indexes=Leve&page={page_num}&string={urllib.parse.quote(leve_name)}'
        )

    @classmethod
    async def xivapi_leve_search(cls, leve_name: str):
        if result := XivApi.cached_responses['Search']['Leve'].get(leve_name):
            return result

        page_num: int = 1
        max_pages: int = 99
        while page_num <= max_pages:
            response = await cls._xivapi_leve_search(leve_name, page_num)
            page_num = response['Pagination']['Page']
            max_pages = response['Pagination']['PageTotal']

            XivApi.cached_responses['Search']['Leve'].setdefault(leve_name, [])
            for result in response['Results']:
                if result['Name'].casefold() == leve_name.casefold():
                    XivApi.cached_responses['Search']['Leve'][leve_name].append(result)

            page_num += 1

        return XivApi.cached_responses['Search']['Leve'][leve_name]

    @classmethod
    async def xivapi_place_name_lookup(cls, place_id: int):
        if result := XivApi.cached_responses['PlaceName'].get(place_id):
            return result

        data = await cls.get_json_at_url(f'https://xivapi.com/PlaceName/{place_id}')
        XivApi.cached_responses['PlaceName'][place_id] = data
        return data

    @classmethod
    async def xivapi_place_name_search(cls, place_name: str):
        if (result := XivApi.cached_responses['Search']['PlaceName'].get(place_name)) is not None:
            return result

        response = await cls.get_json_at_url(
            f'https://xivapi.com/search?indexes=PlaceName&string={urllib.parse.quote(place_name)}'
        )

        XivApi.cached_responses['Search']['PlaceName'].setdefault(place_name, [])
        for result in response['Results']:
            if result['Name'].casefold() == place_name.casefold():
                XivApi.cached_responses['Search']['PlaceName'][place_name].append(result)

        return XivApi.cached_responses['Search']['PlaceName'][place_name]

    @classmethod
    async def xivapi_spearfishing_notebook_lookup(cls, spearfishing_notebook_id: int):
        if result := XivApi.cached_responses['SpearfishingNotebook'].get(spearfishing_notebook_id):
            return result

        data = await cls.get_json_at_url(f'https://xivapi.com/SpearfishingNotebook/{spearfishing_notebook_id}')
        XivApi.cached_responses['SpearfishingNotebook'][spearfishing_notebook_id] = data
        return data

    @classmethod
    async def xivapi_spearfishing_item_lookup(cls, spearfishing_item_id: int):
        if result := XivApi.cached_responses['SpearfishingItem'].get(spearfishing_item_id):
            return result

        data = await cls.get_json_at_url(f'https://xivapi.com/SpearfishingItem/{spearfishing_item_id}')
        XivApi.cached_responses['SpearfishingItem'][spearfishing_item_id] = data
        return data

    @classmethod
    async def xivapi_special_shop_lookup(cls, special_shop_id: int):
        if result := XivApi.cached_responses['SpecialShop'].get(special_shop_id):
            return result

        data = await cls.get_json_at_url(f'https://xivapi.com/SpecialShop/{special_shop_id}')
        XivApi.cached_responses['SpecialShop'][special_shop_id] = data
        return data
