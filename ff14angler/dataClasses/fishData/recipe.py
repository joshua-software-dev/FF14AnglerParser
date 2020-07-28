#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Dict

from bs4.element import Tag

from ...aiohttpWrapped import AiohttpWrapped


@dataclass
class Recipe:
    recipe_angler_crafting_class: str
    recipe_angler_lodestone_url: str
    recipe_angler_name: str
    recipe_icon: str
    recipe_item_id: int
    recipe_name: str

    def __json__(self):
        return self.__dict__

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
    async def get_recipe_from_soup(cls, soup: Tag) -> 'Recipe':
        _, td2, td3, td4 = soup.find_all('td')  # type: _, Tag, Tag, Tag
        angler_item_name = td3.text.strip()

        response = await AiohttpWrapped.xivapi_item_search(angler_item_name)
        item_icon: str = response['Icon']
        item_id: int = response['ID']
        item_name: str = response['Name']

        # noinspection SpellCheckingInspection
        return cls(
            recipe_angler_crafting_class=await cls._parse_crafting_class(td2),
            recipe_angler_lodestone_url=td4.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href'],
            recipe_angler_name=angler_item_name,
            recipe_icon=item_icon,
            recipe_item_id=item_id,
            recipe_name=item_name
        )
