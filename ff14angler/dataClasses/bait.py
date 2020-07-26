#! /usr/bin/env python3

from dataclasses import dataclass

from bs4.element import Tag


@dataclass
class Bait:
    bait_percentage: str = None
    icon_url: str = None
    item_level: int = None
    large_icon_url: str = None
    lodestone_url: str = None
    name: str = None

    @classmethod
    def get_bait_from_soup(cls, soup: Tag) -> 'Bait':
        td1, td2, td3, td4 = soup.find_all('td')  # type: Tag, Tag, Tag, Tag

        bait = cls()
        bait.bait_percentage = td1.text.strip()
        bait.icon_url = td2.find('img').attrs['src']
        bait.item_level = int(td3.text.strip())
        bait.lodestone_url = td4.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href']
        bait.name = td2.text.strip()
        bait.large_icon_url = bait.icon_url.replace('.png', 'l.png')

        return bait
