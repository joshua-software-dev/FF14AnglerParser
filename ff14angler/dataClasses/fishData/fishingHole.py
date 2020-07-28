#! /usr/bin/env python3

import re

from dataclasses import dataclass
from typing import List, Optional, Tuple

from bs4.element import Tag

from ...aiohttpWrapped import AiohttpWrapped


area_regex = re.compile(r"area=([0-9]+)&")
x_coord_regex = re.compile(r"x=([0-9]+)&")
y_coord_regex = re.compile(r"y=([0-9]+)")
number_regex = re.compile(r"[^\d]")


@dataclass
class FishingHole:
    fishing_hole_angler_area_id: int
    fishing_hole_angler_spot_id: int
    fishing_hole_angler_spot_name: str
    fishing_hole_angler_x: int  # yes, really, angler measures in x/y and xivapi is in x/z, I think they both map to
    fishing_hole_angler_y: int  # the horizontal and vertical axises on the in game map
    fishing_hole_fishing_spot_id: int
    fishing_hole_level: int
    fishing_hole_place_name: str
    fishing_hole_place_name_id: int
    fishing_hole_x: int
    fishing_hole_z: int

    def __json__(self):
        return self.__dict__

    @staticmethod
    async def _parse_angler_area_id(td3: Tag) -> int:
        href = td3.find('a').attrs['href']
        match = area_regex.search(href)
        return int(match.groups()[0])

    @staticmethod
    async def _parse_fishing_hole_x(td3: Tag) -> int:
        href = td3.find('a').attrs['href']
        match = x_coord_regex.search(href)
        try:
            return int(match.groups()[0])
        except:
            print(td3)
            raise

    @staticmethod
    async def _parse_fishing_hole_y(td3: Tag) -> int:
        href = td3.find('a').attrs['href']
        match = y_coord_regex.search(href)
        try:
            return int(match.groups()[0])
        except:
            print(td3)
            raise

    @staticmethod
    async def _lookup_place_name_id_and_fishing_hole_id_by_name(fishing_hole_name: str) -> Tuple[int, int]:
        fishing_hole_ids: Optional[List[int]] = None
        place_name_id: Optional[int] = None

        place_search_response = await AiohttpWrapped.xivapi_place_name_search(fishing_hole_name)
        for result in place_search_response['Results']:
            place_name_id = result['ID']
            place_lookup_response = await AiohttpWrapped.xivapi_place_name_lookup(place_name_id)

            try:
                fishing_hole_ids = place_lookup_response['GameContentLinks']['FishingSpot']['PlaceName']
            except KeyError:
                continue

            if len(fishing_hole_ids) != 1:
                raise ValueError(f'Too many fishing holes for place lookup! {place_lookup_response}')

            return place_name_id, fishing_hole_ids[0]

    @classmethod
    async def get_fishing_hole_from_soup(cls, soup: Tag) -> 'FishingHole':
        td1, td2, td3 = soup.find_all('td')  # type: Tag, Tag, Tag
        fishing_hole_name: str = td1.text.strip()

        place_name_id, fishing_hole_id = await cls._lookup_place_name_id_and_fishing_hole_id_by_name(fishing_hole_name)
        hole_lookup_response = await AiohttpWrapped.xivapi_fishing_spot_lookup(fishing_hole_id)

        return cls(
            fishing_hole_angler_area_id=await cls._parse_angler_area_id(td3),
            fishing_hole_angler_spot_id=int(number_regex.sub(repl='', string=td1.find('a').attrs['href'])),
            fishing_hole_angler_spot_name=fishing_hole_name,
            fishing_hole_angler_x=await cls._parse_fishing_hole_x(td3),
            fishing_hole_angler_y=await cls._parse_fishing_hole_y(td3),
            fishing_hole_fishing_spot_id=fishing_hole_id,
            fishing_hole_level=hole_lookup_response['GatheringLevel'],
            fishing_hole_place_name=hole_lookup_response['PlaceName']['Name_en'],
            fishing_hole_place_name_id=place_name_id,
            fishing_hole_x=hole_lookup_response['X'],
            fishing_hole_z=hole_lookup_response['Z']
        )
