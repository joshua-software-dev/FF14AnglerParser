#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Optional

from bs4.element import Tag

from ...aiohttpWrapped import AiohttpWrapped


@dataclass
class Recipe:
    recipe_angler_item_name: str
    recipe_crafting_class: str
    recipe_icon: str
    recipe_lodestone_url: str
    recipe_xivapi_item_id: int
    recipe_xivapi_name: str

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
        td1, td2, td3, td4 = soup.find_all('td')  # type: Tag, Tag, Tag, Tag
        angler_item_name = td3.text.strip()
        item_id: Optional[int] = None
        item_name: Optional[str] = None

        response = await AiohttpWrapped.xivapi_item_search(angler_item_name)
        for result in response['Results']:
            if result['Name'].casefold() == angler_item_name.casefold():
                item_id = result['ID']
                item_name = result['Name']
                break

        if item_id is None or item_name is None:
            raise ValueError(f'Could not find xivapi item for item: {angler_item_name}')

        # noinspection SpellCheckingInspection
        return cls(
            recipe_angler_item_name=angler_item_name,
            recipe_crafting_class=await cls._parse_crafting_class(td2),
            recipe_icon='https://en.ff14angler.com{}'.format(td1.find('img').attrs['src']),
            recipe_lodestone_url=td4.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href'],
            recipe_xivapi_item_id=item_id,
            recipe_xivapi_name=item_name
        )
