#! /usr/bin/env python3

import asyncio

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, TYPE_CHECKING

from bs4 import BeautifulSoup
from bs4.element import Tag

from ff14angler.aiohttpWrapped import AiohttpWrapped
from ff14angler.constants.data_corrections import angler_spot_name_corrections
from ff14angler.constants.regex import (
    angler_map_area_matcher_regex,
    angler_map_x_coord_matcher_regex,
    angler_map_y_coord_matcher_regex,
    non_number_replacement_regex
)
from ff14angler.dataClasses.comment.commentSection import CommentSection
from ff14angler.dataClasses.fish.fishId import FishId
from ff14angler.dataClasses.spot.spotGatheringType import SpotGatheringType

if TYPE_CHECKING:
    # Avoiding circular imports
    from ff14angler.dataClasses.fish.fishProvider import FishProvider


@dataclass
class Spot:
    spot_angler_area_id: Optional[int] = None
    spot_angler_available_fish: List[FishId] = field(default_factory=list)
    spot_angler_comments: Optional[CommentSection] = None
    spot_angler_gathering_level: Optional[int] = None
    spot_angler_name: Optional[str] = None
    spot_angler_spot_id: Optional[int] = None
    # For some reason, `FishingSpot`s on xivapi use X and Z map coordinates and
    # angler uses X and Y map coordinates. I believe they both map to the in
    # game map's X and Z, but its possible angler's actually maps to some pixel
    # coordinate value on their map images for where they should place the
    # fishing hole.
    spot_angler_x_coord: Optional[int] = None
    spot_angler_y_coord: Optional[int] = None
    spot_angler_zone_name: Optional[str] = None
    spot_gathering_level: Optional[int] = None
    spot_gathering_type: Optional[SpotGatheringType] = None

    def __json__(self):
        return self.__dict__

    @staticmethod
    async def _parse_angler_available_fish(soup: BeautifulSoup):
        # Avoiding circular imports
        from ff14angler.dataClasses.fish.fishProvider import FishProvider

        temp_fish_list: List[FishId] = []
        form = soup.find('form', {'name': 'spot_delete'})
        # noinspection SpellCheckingInspection
        body = form.find_all('tbody')[1]

        for tag in body.find_all('tr'):  # type: Tag
            _, td2, td3, _, _, td6 = tag.find_all('td')  # type: _, Tag, Tag, _, _ , Tag
            fish_angler_id: int = int(non_number_replacement_regex.sub(repl='', string=td2.find('a').attrs['href']))
            fish_angler_name: str = td2.text.strip()
            fish = await FishProvider.get_fish_from_angler_fish(fish_angler_id, fish_angler_name)
            temp_fish_list.append(fish.fish_id)

        return temp_fish_list

    @staticmethod
    async def _parse_angler_area_id(soup: BeautifulSoup) -> int:
        return int(
            angler_map_area_matcher_regex.search(
                soup.find('a', {'class': None, 'rel': None}).attrs['href']
            ).groups()[0]
        )

    @staticmethod
    async def _parse_angler_x_coord(soup: BeautifulSoup) -> int:
        return int(
            angler_map_x_coord_matcher_regex.search(
                soup.find('a', {'class': None, 'rel': None}).attrs['href']
            ).groups()[0]
        )

    @staticmethod
    async def _parse_angler_y_coord(soup: BeautifulSoup) -> int:
        return int(
            angler_map_y_coord_matcher_regex.search(
                soup.find('a', {'class': None, 'rel': None}).attrs['href']
            ).groups()[0]
        )

    @staticmethod
    async def _check_if_is_spearfishing_spot(soup: BeautifulSoup) -> bool:
        for tag in soup.find('table', {'id': 'effective_bait'}).find_all('tr'):  # type: Tag
            bait_span = tag.find('span', {'class': 'clear_icon'})
            if bait_span:
                bait_id: str = non_number_replacement_regex.sub(repl='', string=bait_span.find('img').attrs['src'])
                if bait_id in {'2001', '2002', '2003'}:
                    return True

        return False

    async def update_spot_with_assume_is_fishing_spot(self):
        if angler_spot_name_corrections.get(self.spot_angler_name):
            search_name: str = angler_spot_name_corrections.get(self.spot_angler_name)
        else:
            search_name: str = self.spot_angler_name

        place_search_responses = await AiohttpWrapped.xivapi_place_name_search(search_name)
        for place_search_response in place_search_responses:
            place_lookup_response = await AiohttpWrapped.xivapi_place_name_lookup(place_search_response['ID'])
            fishing_spot = place_lookup_response['GameContentLinks'].get('FishingSpot')
            if fishing_spot and fishing_spot.get('PlaceName'):
                spot_lookup_response = await AiohttpWrapped.xivapi_fishing_spot_lookup(
                    max(fishing_spot['PlaceName'])
                )

                self.spot_gathering_level = spot_lookup_response['GatheringLevel']
                # TODO: Replace string for type init with Enum class
                self.spot_gathering_type = SpotGatheringType.get_spot_gathering_type('rod', spot_lookup_response['ID'])

                return

        raise ValueError(f'Could not find fishing spot for spot: {self}')

    async def _lookup_spearfishing_ids_for_available_fish(self) -> Set[int]:
        item_lookups = await asyncio.gather(
            *(
                AiohttpWrapped.xivapi_item_lookup(
                    fish_id.fish_xivapi_item_id
                ) for fish_id in self.spot_angler_available_fish
            )
        )

        spearfishing_item_ids: Set[int] = set()
        for lookup in item_lookups:
            spearfishing_data: Dict[str, List[int]] = lookup['GameContentLinks'].get('SpearfishingItem')

            if spearfishing_data and len(spearfishing_data['Item']) == 1:
                spearfishing_item_ids.add(max(spearfishing_data['Item']))

        return spearfishing_item_ids

    async def update_spot_with_assume_is_teeming_spot(self):
        spearfishing_gpb: List[Tuple[Set[int], int, int]] = (
            await AiohttpWrapped.xivapi_spearfishing_gathering_point_base_index()
        )

        spearfishing_ids = await self._lookup_spearfishing_ids_for_available_fish()
        for gpb_known_fish, gpb_id, gpb_level in spearfishing_gpb:
            # If a gathering point base and this spot share 2 or more fish as being known to be caught there...
            if len(gpb_known_fish.intersection(spearfishing_ids)) >= 2:
                self.spot_gathering_level = gpb_level
                self.spot_gathering_type = SpotGatheringType.get_spot_gathering_type('teeming', gpb_id)
                return

        raise ValueError(f'Could not find GatheringPointBase for spot: {self}')

    async def update_spot_with_assume_is_spearfishing_spot(self):
        if angler_spot_name_corrections.get(self.spot_angler_name):
            search_name: str = angler_spot_name_corrections.get(self.spot_angler_name)
        else:
            search_name: str = self.spot_angler_name

        place_search_responses = await AiohttpWrapped.xivapi_place_name_search(search_name)

        for place_search_response in place_search_responses:
            place_lookup_response = await AiohttpWrapped.xivapi_place_name_lookup(place_search_response['ID'])
            notebook = place_lookup_response['GameContentLinks'].get('SpearfishingNotebook')
            if notebook:
                spearfishing_ids: List[int] = notebook['PlaceName']

                if len(spearfishing_ids) != 1:
                    raise ValueError(f'Too many SpearfishingNotebook ids for spot! {self}')

                notebook_lookup = await AiohttpWrapped.xivapi_spearfishing_notebook_lookup(max(spearfishing_ids))
                self.spot_gathering_level = notebook_lookup['GatheringLevel']
                self.spot_gathering_type = SpotGatheringType.get_spot_gathering_type('spear', notebook_lookup['ID'])
                return

        return await self.update_spot_with_assume_is_teeming_spot()

    async def update_spot_with_spot_soup(self, soup: BeautifulSoup) -> 'Spot':
        spot_info: Tag = soup.find('table', {'class': 'spot_info'})

        self.spot_angler_area_id = await self._parse_angler_area_id(spot_info)
        self.spot_angler_available_fish = await self._parse_angler_available_fish(soup)
        self.spot_angler_gathering_level = int(
            non_number_replacement_regex.sub(repl='', string=spot_info.find('span', {'class': 'level'}).text)
        )
        self.spot_angler_x_coord = await self._parse_angler_x_coord(spot_info)
        self.spot_angler_y_coord = await self._parse_angler_y_coord(spot_info)

        if await self._check_if_is_spearfishing_spot(soup):
            await self.update_spot_with_assume_is_spearfishing_spot()
        else:
            await self.update_spot_with_assume_is_fishing_spot()

        return self

    async def update_spot_with_comment_section(self, comment_section: CommentSection):
        self.spot_angler_comments = comment_section
