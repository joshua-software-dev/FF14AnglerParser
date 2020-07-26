#! /usr/bin/env python3

import re

from dataclasses import dataclass

from bs4.element import Tag


@dataclass
class FishingHole:
    fishing_hole_angler_area_id: int = None
    fishing_hole_angler_spot_id: int = None
    fishing_hole_level: int = None
    fishing_hole_name: str = None
    fishing_hole_x: int = None
    fishing_hole_y: int = None

    def __json__(self):
        return self.__dict__

    @staticmethod
    def _parse_angler_area_id(td3: Tag) -> int:
        href = td3.find('a').attrs['href']
        match = re.search(r"area=([0-9]+)&", href)
        return int(match.groups()[0])

    @staticmethod
    def _parse_fishing_hole_x(td3: Tag) -> int:
        href = td3.find('a').attrs['href']
        match = re.search(r"x=([0-9]+)&", href)
        return int(match.groups()[0])

    @staticmethod
    def _parse_fishing_hole_y(td3: Tag) -> int:
        href = td3.find('a').attrs['href']
        match = re.search(r"y=([0-9]+)", href)
        return int(match.groups()[0])

    @classmethod
    def get_fishing_hole_from_soup(cls, soup: Tag) -> 'FishingHole':
        try:
            td1, td2, td3 = soup.find_all('td')
        except:
            print(soup.find_all('td'))

        fishing_hole = cls()
        fishing_hole.fishing_hole_angler_area_id = cls._parse_angler_area_id(td3)
        fishing_hole.fishing_hole_angler_spot_id = int(re.sub(r"[^0-9]", '', td1.find('a').attrs['href']))
        fishing_hole.fishing_hole_level = int(td2.text.strip())
        fishing_hole.fishing_hole_name = td1.text.strip()
        fishing_hole.fishing_hole_x = cls._parse_fishing_hole_x(td3)
        fishing_hole.fishing_hole_y = cls._parse_fishing_hole_y(td3)

        return fishing_hole
