#! /usr/bin/env python3

from dataclasses import dataclass

from bs4.element import Tag

from ...aiohttpWrapped import AiohttpWrapped


@dataclass
class DesynthesisChance:
    desynthesis_angler_item_name: str
    desynthesis_angler_lodestone_url: str
    desynthesis_angler_percentage: str
    desynthesis_icon_url: str
    desynthesis_item_id: int
    desynthesis_item_name: str

    def __json__(self):
        return self.__dict__

    @classmethod
    async def get_desynthesis_chance_from_soup(cls, soup: Tag) -> 'DesynthesisChance':
        td1, td2, td3 = soup.find_all('td')  # type: Tag, Tag, Tag
        angler_item_name = td2.text.strip()

        response = await AiohttpWrapped.xivapi_item_search(angler_item_name)

        # noinspection SpellCheckingInspection
        return cls(
            desynthesis_angler_item_name=angler_item_name,
            desynthesis_angler_lodestone_url=td3.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href'],
            desynthesis_angler_percentage=td1.text.strip(),
            desynthesis_icon_url=f'https://xivapi.com{response["Icon"]}',
            desynthesis_item_id=response['ID'],
            desynthesis_item_name=response['Name']
        )
