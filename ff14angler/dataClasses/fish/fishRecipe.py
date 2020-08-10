#! /usr/bin/env python3

import urllib.parse

from dataclasses import dataclass
from typing import Dict, Optional

from bs4.element import Tag  # type: ignore

from ff14angler.aiohttpWrapped import AiohttpWrapped
from ff14angler.constants.values import ANGLER_API_BASE_URL


@dataclass
class FishRecipe:
    recipe_angler_crafting_class: str
    recipe_angler_lodestone_url: str
    recipe_angler_name: str
    recipe_icon_url: str
    recipe_item_id: int
    recipe_name: str
    recipe_large_icon_url: Optional[str] = None

    @staticmethod
    async def _parse_crafting_class(td2: Tag) -> str:
        # noinspection SpellCheckingInspection
        _lookup: Dict[str, str] = {
            '/img/i_relavant001.png': 'CRP',
            '/img/i_relavant002.png': 'BSM',
            '/img/i_relavant003.png': 'ARM',
            '/img/i_relavant004.png': 'GSM',
            '/img/i_relavant005.png': 'LTW',
            # There is no weaver image for some reason
            '/img/i_relavant007.png': 'ALC',
            '/img/i_relavant008.png': 'CUL'
        }

        return _lookup[td2.find('img').attrs['src']]

    @classmethod
    async def get_recipe_from_fish_soup(cls, soup: Tag) -> 'FishRecipe':
        _, td2, td3, td4 = soup.find_all('td')  # type: _, Tag, Tag, Tag
        angler_item_name = td3.text.strip()
        response = await AiohttpWrapped.xivapi_item_search(angler_item_name)

        # noinspection SpellCheckingInspection
        return cls(
            recipe_angler_crafting_class=await cls._parse_crafting_class(td2),
            recipe_angler_lodestone_url=td4.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href'],
            recipe_angler_name=angler_item_name,
            recipe_icon_url=urllib.parse.urljoin(ANGLER_API_BASE_URL, response["Icon"].lstrip('/')),
            recipe_item_id=response['ID'],
            recipe_name=response['Name']
        )
