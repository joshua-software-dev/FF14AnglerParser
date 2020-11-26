#! /usr/bin/env python3

from typing import Dict, List, Optional

from bs4 import BeautifulSoup  # type: ignore
from bs4.element import Tag  # type: ignore

from ff14angler.constants.regex import mooch_name_regex, non_number_replacement_regex
from ff14angler.dataClasses.bait.bait import Bait
from ff14angler.dataClasses.bait.baitPercentage import BaitPercentage


class BaitProvider:
    bait_holder: Dict[int, Bait] = dict()

    @staticmethod
    async def _parse_angler_bait_id(td2: Tag) -> int:
        a_tag = td2.find('a')
        if a_tag:
            return int(non_number_replacement_regex.sub(repl='', string=a_tag.attrs['href']))
        return int(non_number_replacement_regex.sub(repl='', string=td2.find('img').attrs['src']))

    @classmethod
    async def get_bait_from_angler_bait(cls, bait_angler_id: int, bait_angler_name: str) -> Bait:
        if result := cls.bait_holder.get(bait_angler_id):
            return result

        cls.bait_holder[bait_angler_id] = await Bait.get_bait_from_angler_bait(
            bait_angler_id=bait_angler_id,
            bait_angler_name=bait_angler_name
        )
        return cls.bait_holder[bait_angler_id]

    @classmethod
    async def get_bait_percentage_list_from_fish_soup(cls, soup: BeautifulSoup) -> List[BaitPercentage]:
        temp_bait_list: List[BaitPercentage] = []

        bait_section: Optional[Tag] = soup.find('form', {'name': 'bait_delete'})
        if not bait_section:
            return temp_bait_list

        for child in bait_section.find_all('td', {'class': 'width_max'}):  # type: Tag
            parent: Tag = child.parent
            td1, td2 = parent.find_all('td')[:2]  # type: Tag, Tag
            angler_bait_id: int = await cls._parse_angler_bait_id(td2)
            angler_bait_name: str = mooch_name_regex.sub('', td2.text).strip()
            bait = await cls.get_bait_from_angler_bait(angler_bait_id, angler_bait_name)

            if bait.bait_item_name_en is None:
                await bait.update_bait_with_assume_is_mooch_fish()

            temp_bait_list.append(
                BaitPercentage(
                    bait_id=bait.bait_id,
                    bait_percentage=td1.text.strip()
                )
            )

        return temp_bait_list
