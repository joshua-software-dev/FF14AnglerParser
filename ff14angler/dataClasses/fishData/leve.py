#! /usr/bin/env python3

import re

from dataclasses import dataclass
from typing import Optional

from bs4.element import Tag

from ...aiohttpWrapped import AiohttpWrapped


@dataclass
class Leve:
    leve_angler_fish_id: int
    leve_angler_fish_name: str
    leve_level: int
    leve_name: str
    leve_name_jp: str
    leve_turn_in_count: int
    leve_xivapi_item_id: int
    leve_xivapi_item_name: str

    def __json__(self):
        return self.__dict__

    @staticmethod
    async def _parse_leve_name(td1: Tag) -> str:
        td1.find('font').decompose()
        if quest_text := td1.find('div'):
            quest_text.decompose()
        return td1.text.strip()

    @classmethod
    async def get_leve_from_soup(cls, soup: Tag) -> 'Leve':
        td1, td2, td3, td4, _ = soup.find_all('td')  # type: Tag, Tag, Tag, Tag, _
        angler_fish_name = td3.text.strip()
        item_id: Optional[int] = None
        item_name: Optional[str] = None

        response = await AiohttpWrapped.xivapi_item_search(angler_fish_name)
        for result in response['Results']:
            if result['Name'].casefold() == angler_fish_name.casefold():
                item_id = result['ID']
                item_name = result['Name']
                break

        if item_id is None or item_name is None:
            raise ValueError(f'Could not find xivapi item for item: {angler_fish_name}')

        return cls(
            leve_angler_fish_id=int(td3.find('a').attrs['href'].split('/')[-1]),
            leve_angler_fish_name=angler_fish_name,
            leve_level=td2.text.strip(),
            leve_name_jp=td1.find('font').text.strip(),
            leve_name=await cls._parse_leve_name(td1),
            leve_turn_in_count=int(re.sub(pattern=r"[^0-9]", repl='', string=td4.text)),
            leve_xivapi_item_id=item_id,
            leve_xivapi_item_name=item_name
        )
