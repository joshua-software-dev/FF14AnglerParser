#! /usr/bin/env python3

from dataclasses import dataclass

from bs4.element import Tag

from ff14angler.aiohttpWrapped import AiohttpWrapped
from ff14angler.constants.regex import non_number_replacement_regex


@dataclass
class FishLeve:
    leve_angler_fish_id: int
    leve_angler_fish_name: str
    leve_angler_name: str
    leve_angler_name_jp: str
    leve_angler_turn_in_count: int
    leve_name: str
    leve_id: int
    leve_item_id: int
    leve_item_name: str
    leve_level: int

    def __json__(self):
        return self.__dict__

    @staticmethod
    async def _parse_leve_name(td1: Tag) -> str:
        td1.find('font').decompose()
        if quest_text := td1.find('div'):
            quest_text.decompose()
        return td1.text.strip()

    @classmethod
    async def get_leve_from_soup(cls, soup: Tag) -> 'FishLeve':
        td1, _, td3, td4, _ = soup.find_all('td')  # type: Tag, _, Tag, Tag, _
        angler_leve_name_jp: str = td1.find('font').text.strip()
        angler_leve_name: str = await cls._parse_leve_name(td1)

        search_responses = await AiohttpWrapped.xivapi_leve_search(angler_leve_name)
        for search_response in search_responses:
            lookup_response = await AiohttpWrapped.xivapi_leve_lookup(search_response['ID'])
            if lookup_response['CraftLeve']:
                return cls(
                    leve_angler_fish_id=int(td3.find('a').attrs['href'].split('/')[-1]),
                    leve_angler_fish_name=td3.text.strip(),
                    leve_angler_name=angler_leve_name,
                    leve_angler_name_jp=angler_leve_name_jp,
                    leve_angler_turn_in_count=int(non_number_replacement_regex.sub(repl='', string=td4.text)),
                    leve_name=lookup_response['Name_en'],
                    leve_id=lookup_response['ID'],
                    leve_item_id=lookup_response['CraftLeve']['Item0']['ID'],
                    leve_item_name=lookup_response['CraftLeve']['Item0']['Name_en'],
                    leve_level=lookup_response['ClassJobLevel']
                )

        raise ValueError(f'Could not find applicable leve for leve name: {angler_leve_name}')
