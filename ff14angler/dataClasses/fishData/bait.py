#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Optional

from bs4.element import Tag

from ...aiohttpWrapped import AiohttpWrapped


@dataclass
class Bait:
    bait_angler_bait_id: int
    bait_angler_name: str
    bait_icon_url: str
    bait_item_level: int
    bait_name: str
    bait_xivapi_item_id: int

    bait_large_icon_url: str = None
    bait_lodestone_url: str = None
    bait_percentage: str = None

    def __json__(self):
        return self.__dict__

    async def update_with_soup(self, td1: Tag, td2: Tag, td4: Tag) -> 'Bait':
        self.bait_large_icon_url = 'https://en.ff14angler.com{}'.format(
            td2.find('img').attrs['src'].replace('.png', 'l.png')
        )

        # noinspection SpellCheckingInspection
        self.bait_lodestone_url = td4.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href']
        self.bait_percentage = td1.text.strip()

        return self

    @classmethod
    async def get_bait_from_angler_name(cls, bait_name: str, angler_id: int = None) -> 'Bait':
        # noinspection SpellCheckingInspection
        name_corrections: Dict[str, str] = {
            'fistful of northern krill': 'northern krill',
            'pot of salmon roe': 'salmon roe',
            'strip of jerked ovim': 'jerked ovim',
            'box of baitbugs': 'baitbugs'
        }

        bait_xivapi_item_id: Optional[int] = None
        bait_search_name = name_corrections.get(bait_name) or bait_name

        search_response = await AiohttpWrapped.xivapi_item_search(bait_search_name)
        for result in search_response['Results']:
            if result['Name'].casefold() == bait_search_name.casefold():
                bait_xivapi_item_id: int = result['ID']
                break

        lookup_response = await AiohttpWrapped.xivapi_item_lookup(bait_xivapi_item_id)

        return cls(
            bait_angler_bait_id=angler_id,
            bait_angler_name=bait_name,
            bait_icon_url=f'https://xivapi.com{lookup_response["Icon"]}',
            bait_item_level=lookup_response['LevelItem'],
            bait_name=lookup_response['Name_en'],
            bait_xivapi_item_id=lookup_response['ID']
        )
