#! /usr/bin/env python3

import re

from typing import Dict, List

from bs4 import BeautifulSoup
from bs4.element import Tag

from .bait import Bait
from .baitPercentage import BaitPercentage


non_number_match_regex = re.compile(r"[^\d]")


class BaitProvider:
    bait_holder: Dict[int, Bait] = dict()

    @classmethod
    def __json__(cls):
        return cls.bait_holder

    @staticmethod
    async def _parse_angler_bait_id(td2: Tag) -> int:
        a_tag = td2.find('a')
        if a_tag:
            return int(non_number_match_regex.sub(repl='', string=a_tag.attrs['href']))
        return int(non_number_match_regex.sub(repl='', string=td2.find('img').attrs['src']))

    @classmethod
    async def get_bait_from_angler_bait(cls, bait_angler_id: int, bait_angler_name: str) -> Bait:
        if result := cls.bait_holder.get(bait_angler_id):
            return result

        cls.bait_holder[bait_angler_id] = Bait(bait_angler_id=bait_angler_id, bait_angler_name=bait_angler_name)
        return cls.bait_holder[bait_angler_id]

    @classmethod
    async def get_bait_percentage_list_from_fish_soup(cls, soup: BeautifulSoup) -> List[BaitPercentage]:
        temp_bait_list: List[BaitPercentage] = []

        for tr in soup.find_all('tr', {'class': 'bait'}):  # type: Tag
            td1, td2, _, td4 = tr.find_all('td')  # type: Tag, Tag, _, Tag
            angler_bait_id: int = await cls._parse_angler_bait_id(td2)
            angler_bait_name: str = td2.text.strip()
            bait = await cls.get_bait_from_angler_bait(angler_bait_id, angler_bait_name)
            temp_bait_list.append(BaitPercentage(bait=bait, bait_percentage=td1.text.strip()))

        return temp_bait_list
