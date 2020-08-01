#! /usr/bin/env python3

import re

from dataclasses import dataclass
from typing import Optional

from bs4.element import Tag

from ff14angler.aiohttpWrapped import AiohttpWrapped


quantity_regex = re.compile(r"\((\s+)?\d+(\s+)?~(\s+)?\d+(\s+)?\)$")


@dataclass
class FishDesynthesisChance:
    desynthesis_angler_item_name: str
    desynthesis_angler_lodestone_url: str
    desynthesis_angler_percentage: str
    desynthesis_icon_url: str
    desynthesis_item_id: int
    desynthesis_item_name: str

    def __json__(self):
        return self.__dict__

    @staticmethod
    async def _parse_angler_item_name(td2: Tag) -> str:
        return quantity_regex.sub(repl='', string=td2.text.strip()).strip()

    @staticmethod
    async def _read_icon_url(icon: Optional[str]) -> Optional[str]:
        if icon:
            return f'https://xivapi.com{icon}'
        return None

    @staticmethod
    async def _parse_angler_lodestone_url(td3: Tag) -> Optional[str]:
        a_tag = td3.find('a', {'class': 'lodestone eorzeadb_link'})
        if a_tag:
            return a_tag.attrs['href']
        return None

    @classmethod
    async def get_desynthesis_chance_from_soup(cls, soup: Tag) -> 'FishDesynthesisChance':
        td1, td2, td3 = soup.find_all('td')  # type: Tag, Tag, Tag
        angler_item_name: str = await cls._parse_angler_item_name(td2)

        try:
            response = await AiohttpWrapped.xivapi_item_search(angler_item_name)
        except ValueError:
            response = dict()

        # noinspection SpellCheckingInspection
        return cls(
            desynthesis_angler_item_name=angler_item_name,
            desynthesis_angler_lodestone_url=await cls._parse_angler_lodestone_url(td3),
            desynthesis_angler_percentage=td1.text.strip(),
            desynthesis_icon_url=await cls._read_icon_url(response.get('Icon')),
            desynthesis_item_id=response.get('ID'),
            desynthesis_item_name=response.get('Name')
        )
