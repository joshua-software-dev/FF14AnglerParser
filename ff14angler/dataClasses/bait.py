#! /usr/bin/env python3

from dataclasses import dataclass

from bs4.element import Tag


@dataclass
class Bait:
    bait_icon_url: str
    bait_item_level: int
    bait_large_icon_url: str
    bait_lodestone_url: str
    bait_name: str
    bait_percentage: str

    def __json__(self):
        return self.__dict__

    @staticmethod
    def _parse_icon_url(td2: Tag) -> str:
        return td2.find('img').attrs['src']

    @staticmethod
    def _parse_large_icon_url(td2: Tag) -> str:
        return td2.find('img').attrs['src'].replace('.png', 'l.png')

    @classmethod
    def get_bait_from_soup(cls, soup: Tag) -> 'Bait':
        td1, td2, td3, td4 = soup.find_all('td')  # type: Tag, Tag, Tag, Tag

        return cls(
            bait_icon_url=cls._parse_icon_url(td2),
            bait_item_level=int(td3.text.strip()),
            bait_large_icon_url=cls._parse_large_icon_url(td2),
            bait_lodestone_url=td4.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href'],
            bait_name=td2.text.strip(),
            bait_percentage=td1.text.strip()
        )







        return bait
