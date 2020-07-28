#! /usr/bin/env python3

from typing import Dict, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from .fishData import FishData


class FishProvider:
    fish_holder: Dict[str, FishData] = dict()

    @classmethod
    def __json__(cls):
        return cls.fish_holder

    @classmethod
    async def get_fish_data_from_fish_soup(cls, soup: BeautifulSoup) -> FishData:
        fish_table: Tag = soup.find('table', {'class': 'fish_info'})
        angler_fish_name: str = await FishData.parse_angler_fish_name(fish_table.find('tr'))
        fish = await FishData.get_fish_data_from_angler_name(angler_fish_name)
        cls.fish_holder[angler_fish_name] = await fish.update_fish_data_from_fish_soup(soup)
        return cls.fish_holder[angler_fish_name]

    @classmethod
    async def get_fish_data_from_angler_name(cls, fish_name: str, fish_id: Optional[int]) -> FishData:
        if not cls.fish_holder.get(fish_name):
            cls.fish_holder[fish_name] = await FishData.get_fish_data_from_angler_name(fish_name, fish_id)

        return cls.fish_holder[fish_name]
