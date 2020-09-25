#! /usr/bin/env python3

import asyncio
import os

from typing import List, Set
from urllib.parse import urljoin, quote as url_quote

from ff14angler.constants.values import EXPORT_DIRECTORY, XIVAPI_BASE_URL
from ff14angler.dataClasses.cache.xivapiCache import XivapiCache
from ff14angler.dataClasses.cache.idIndexCache import GatheringPointBaseSpearfishingIds
from ff14angler.network.aiohttpWrapper import AiohttpWrapper


class XivapiWrapper:
    cache = XivapiCache()
    connection = AiohttpWrapper(rate_limit=3, duration=3)

    @classmethod
    async def xivapi_download_icon_image(cls, icon_fragment: str):
        output_path: str = os.path.join(EXPORT_DIRECTORY, icon_fragment.lstrip('/'))
        if not os.path.isfile(output_path):
            img_bytes: bytes = await cls.connection.get_bytes_at_url(
                urljoin(
                    XIVAPI_BASE_URL,
                    icon_fragment.lstrip('/')
                )
            )

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb+') as fh:
                fh.write(img_bytes)

    @classmethod
    async def xivapi_fish_parameter_lookup(cls, fish_param_id: int):
        if result := cls.cache.FishParameter.get(fish_param_id):
            return result

        data = await cls.connection.get_json_at_url(urljoin(XIVAPI_BASE_URL, f'FishParameter/{fish_param_id}'))
        cls.cache.FishParameter[fish_param_id] = data
        return data

    @classmethod
    async def xivapi_fishing_spot_lookup(cls, fishing_spot_id: int):
        if result := cls.cache.FishingSpot.get(fishing_spot_id):
            return result

        data = await cls.connection.get_json_at_url(urljoin(XIVAPI_BASE_URL, f'FishingSpot/{fishing_spot_id}'))
        cls.cache.FishingSpot[fishing_spot_id] = data
        return data

    @classmethod
    async def xivapi_gathering_point_lookup(cls, gathering_point_id: int):
        if result := cls.cache.GatheringPoint.get(gathering_point_id):
            return result

        data = await cls.connection.get_json_at_url(
            urljoin(
                XIVAPI_BASE_URL,
                f'GatheringPoint/{gathering_point_id}'
            )
        )
        cls.cache.GatheringPoint[gathering_point_id] = data
        return data

    @classmethod
    async def xivapi_gathering_point_base_index(cls):
        if result := cls.cache.IdIndex.GatheringPointBaseIndex:
            return result

        temp_results = []
        page_num: int = 1

        while True:

            response = await cls.connection.get_json_at_url(
                urljoin(
                    XIVAPI_BASE_URL,
                    f'GatheringPointBase?limit=1000&page={page_num}'
                )
            )
            page_num: int = response['Pagination']['Page']
            max_pages: int = response['Pagination']['PageTotal']
            temp_results += response['Results']

            if page_num >= max_pages:
                cls.cache.IdIndex.GatheringPointBaseIndex = temp_results
                return temp_results

            page_num += 1

    @classmethod
    async def xivapi_gathering_point_base_lookup(cls, gathering_point_base_id: int):
        if result := cls.cache.GatheringPointBase.get(gathering_point_base_id):
            return result

        data = await cls.connection.get_json_at_url(
            urljoin(
                XIVAPI_BASE_URL,
                f'GatheringPointBase/{gathering_point_base_id}'
            )
        )
        cls.cache.GatheringPointBase[gathering_point_base_id] = data
        return data

    @classmethod
    async def xivapi_item_lookup(cls, item_id: int):
        if result := cls.cache.Item.get(item_id):
            return result

        data = await cls.connection.get_json_at_url(urljoin(XIVAPI_BASE_URL, f'Item/{item_id}'))
        cls.cache.Item[item_id] = data
        return data

    @classmethod
    async def xivapi_item_search(cls, item_name: str):
        if result := cls.cache.Search.Item.get(item_name):
            return result

        query = {
            "columns": "Icon,ID,Name_de,Name_en,Name_fr,Name_ja",
            "indexes": "item",
            "body": {
                "query": {
                    "multi_match": {
                        "query": item_name,
                        "fields": ["Name_en", "Name_ja"]
                    }
                }
            }
        }

        response = await cls.connection.post_json_at_url(urljoin(XIVAPI_BASE_URL, 'search'), item_name, query)
        for result in response['Results']:
            for name_language in ['Name_en', 'Name_ja']:
                if result[name_language].casefold() == item_name.casefold():
                    cls.cache.Search.Item[item_name] = result
                    return result

        raise ValueError(f'Could not find applicable result for search term: {item_name}')

    @classmethod
    async def xivapi_leve_lookup(cls, leve_id: int):
        if result := cls.cache.Leve.get(leve_id):
            return result

        data = await cls.connection.get_json_at_url(urljoin(XIVAPI_BASE_URL, f'Leve/{leve_id}'))
        cls.cache.Leve[leve_id] = data
        return data

    @classmethod
    async def xivapi_leve_search(cls, leve_name: str):
        # TODO: Change search to use elastisearch
        if result := cls.cache.Search.Leve.get(leve_name):
            return result

        page_num: int = 1
        max_pages: int = 99
        while page_num <= max_pages:
            response = await cls.connection.get_json_at_url(
                urljoin(
                    XIVAPI_BASE_URL,
                    f'search?indexes=Leve&page={page_num}&string={url_quote(leve_name)}'
                )
            )
            page_num = response['Pagination']['Page']
            max_pages = response['Pagination']['PageTotal']

            cls.cache.Search.Leve.setdefault(leve_name, [])
            for result in response['Results']:
                if result['Name'].casefold() == leve_name.casefold():
                    cls.cache.Search.Leve[leve_name].append(result)

            page_num += 1

        return cls.cache.Search.Leve[leve_name]

    @classmethod
    async def xivapi_place_name_lookup(cls, place_id: int):
        if result := cls.cache.PlaceName.get(place_id):
            return result

        data = await cls.connection.get_json_at_url(urljoin(XIVAPI_BASE_URL, f'PlaceName/{place_id}'))
        cls.cache.PlaceName[place_id] = data
        return data

    @classmethod
    async def xivapi_place_name_search(cls, place_name: str):
        # TODO: Change search to use elastisearch
        if (result := cls.cache.Search.PlaceName.get(place_name)) is not None:
            return result

        response = await cls.connection.get_json_at_url(
            urljoin(
                XIVAPI_BASE_URL,
                f'search?indexes=PlaceName&string={url_quote(place_name)}'
            )
        )

        cls.cache.Search.PlaceName.setdefault(place_name, [])
        for result in response['Results']:
            if result['Name'].casefold() == place_name.casefold():
                cls.cache.Search.PlaceName[place_name].append(result)

        return cls.cache.Search.PlaceName[place_name]

    @classmethod
    async def xivapi_spearfishing_gathering_point_base_index(cls) -> List[GatheringPointBaseSpearfishingIds]:
        if result := cls.cache.IdIndex.GatheringPointBaseSpearfishingIndex:
            return result

        gathering_point_base_spearfishing_spots: List[GatheringPointBaseSpearfishingIds] = []
        index_response = await cls.xivapi_gathering_point_base_index()
        index_lookup = await asyncio.gather(
            *(cls.xivapi_gathering_point_base_lookup(gpb['ID']) for gpb in index_response)
        )

        for gpb_result in index_lookup:
            if gpb_result['GatheringTypeTargetID'] == 4:
                spearfishing_ids: Set[int] = set()
                for i in range(8):
                    if (key := gpb_result.get(f'Item{i}')) not in [0, None]:
                        spearfishing_ids.add(key)

                if spearfishing_ids:
                    gathering_point_base_spearfishing_spots.append(
                        {
                            'game_content_links': gpb_result['GameContentLinks'],
                            'gathering_point_base_id': gpb_result['ID'],
                            'gathering_point_base_level': gpb_result['GatheringLevel'],
                            'spearfishing_ids': spearfishing_ids,
                        }
                    )

        cls.cache.IdIndex.GatheringPointBaseSpearfishingIndex = gathering_point_base_spearfishing_spots
        return gathering_point_base_spearfishing_spots

    @classmethod
    async def xivapi_spearfishing_item_lookup(cls, spearfishing_item_id: int):
        if result := cls.cache.SpearfishingItem.get(spearfishing_item_id):
            return result

        data = await cls.connection.get_json_at_url(
            urljoin(
                XIVAPI_BASE_URL,
                f'SpearfishingItem/{spearfishing_item_id}'
            )
        )
        cls.cache.SpearfishingItem[spearfishing_item_id] = data
        return data

    @classmethod
    async def xivapi_spearfishing_notebook_lookup(cls, spearfishing_notebook_id: int):
        if result := cls.cache.SpearfishingNotebook.get(spearfishing_notebook_id):
            return result

        data = await cls.connection.get_json_at_url(
            urljoin(
                XIVAPI_BASE_URL,
                f'SpearfishingNotebook/{spearfishing_notebook_id}'
            )
        )
        cls.cache.SpearfishingNotebook[spearfishing_notebook_id] = data
        return data

    @classmethod
    async def xivapi_special_shop_lookup(cls, special_shop_id: int):
        if result := cls.cache.SpecialShop.get(special_shop_id):
            return result

        data = await cls.connection.get_json_at_url(
            urljoin(
                XIVAPI_BASE_URL,
                f'SpecialShop/{special_shop_id}'
            )
        )
        cls.cache.SpecialShop[special_shop_id] = data
        return data
