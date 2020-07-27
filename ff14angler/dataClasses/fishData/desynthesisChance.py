#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Optional

from bs4.element import Tag

from ...aiohttpWrapped import AiohttpWrapped


@dataclass
class DesynthesisChance:
    desynthesis_angler_item_name: str
    desynthesis_icon_url: str
    desynthesis_lodestone_url: str
    desynthesis_percentage: str
    desynthesis_xivapi_item_id: int
    desynthesis_xivapi_item_name: str

    def __json__(self):
        return self.__dict__

    @classmethod
    async def get_desynthesis_chance_from_soup(cls, soup: Tag) -> 'DesynthesisChance':
        td1, td2, td3 = soup.find_all('td')  # type: Tag, Tag, Tag
        angler_item_name = td2.text.strip()
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
            desynthesis_angler_item_name=angler_item_name,
            desynthesis_icon_url='https://en.ff14angler.com{}'.format(td2.find('img').attrs['src']),
            desynthesis_lodestone_url=td3.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href'],
            desynthesis_percentage=td1.text.strip(),
            desynthesis_xivapi_item_id=item_id,
            desynthesis_xivapi_item_name=item_name
        )
