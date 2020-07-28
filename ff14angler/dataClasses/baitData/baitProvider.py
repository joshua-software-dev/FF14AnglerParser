#! /usr/bin/env python3

from typing import Dict, List

from bs4 import BeautifulSoup
from bs4.element import Tag

from .baitData import BaitData


class BaitProvider:
    bait_holder: Dict[str, BaitData] = dict()

    @classmethod
    def __json__(cls):
        return cls.bait_holder

    @classmethod
    async def get_bait_data_from_bait_soup(cls, soup: BeautifulSoup) -> BaitData:
        raise NotImplementedError

    @classmethod
    async def get_bait_data_list_from_fish_soup(cls, soup: BeautifulSoup) -> List[BaitData]:
        temp_bait_list: List[BaitData] = []

        for tr in soup.find_all('tr', {'class': 'bait'}):  # type: Tag
            td1, td2, _, td4 = tr.find_all('td')  # type: Tag, Tag, _, Tag
            bait_name: str = td2.text.strip()
            bait = await cls.get_bait_data_from_angler_name(bait_name)
            cls.bait_holder[bait_name] = await bait.update_bait_with_fish_soup(td1, td2, td4)
            temp_bait_list.append(cls.bait_holder[bait_name])

        return temp_bait_list

    @classmethod
    async def get_bait_data_from_angler_name(cls, bait_name: str) -> BaitData:
        if not cls.bait_holder.get(bait_name):
            cls.bait_holder[bait_name] = await BaitData.get_bait_from_angler_name(bait_name)

        return cls.bait_holder[bait_name]
