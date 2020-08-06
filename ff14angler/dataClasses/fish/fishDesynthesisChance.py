#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Optional

from bs4.element import Tag  # type: ignore

from ff14angler.aiohttpWrapped import AiohttpWrapped
from ff14angler.constants.data_corrections import angler_desynthesis_item_name_corrections
from ff14angler.constants.regex import desynthesis_quantity_matcher_regex


@dataclass
class FishDesynthesisChance:
    desynthesis_angler_item_name: str
    desynthesis_angler_lodestone_url: Optional[str]
    desynthesis_angler_percentage: str
    desynthesis_icon_url: str
    desynthesis_item_id: int
    desynthesis_item_name: str

    def __json__(self):
        return self.__dict__

    @staticmethod
    async def _parse_angler_item_name(td2: Tag) -> str:
        return desynthesis_quantity_matcher_regex.sub(repl='', string=td2.text.strip()).strip()

    @staticmethod
    async def _parse_angler_lodestone_url(td3: Tag) -> Optional[str]:
        # noinspection SpellCheckingInspection
        a_tag = td3.find('a', {'class': 'lodestone eorzeadb_link'})
        if a_tag:
            return a_tag.attrs['href']
        return None

    @classmethod
    async def get_desynthesis_chance_from_soup(cls, soup: Tag) -> 'FishDesynthesisChance':
        td1, td2, td3 = soup.find_all('td')  # type: Tag, Tag, Tag
        angler_item_name: str = await cls._parse_angler_item_name(td2)

        response = await AiohttpWrapped.xivapi_item_search(
            angler_desynthesis_item_name_corrections.get(angler_item_name) or angler_item_name
        )

        # noinspection SpellCheckingInspection
        return cls(
            desynthesis_angler_item_name=angler_item_name,
            desynthesis_angler_lodestone_url=await cls._parse_angler_lodestone_url(td3),
            desynthesis_angler_percentage=td1.text.strip(),
            desynthesis_icon_url=f'https://xivapi.com{response["Icon"]}',
            desynthesis_item_id=response['ID'],
            desynthesis_item_name=response['Name']
        )
