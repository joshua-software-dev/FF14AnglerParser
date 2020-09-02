#! /usr/bin/env python3

import asyncio

from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from bs4 import BeautifulSoup  # type: ignore
from bs4.element import Tag  # type: ignore
from dataclasses_json import DataClassJsonMixin

from ff14angler.constants.data_corrections import angler_spot_name_corrections
from ff14angler.constants.regex import (
    angler_map_area_matcher_regex,
    angler_map_x_coord_matcher_regex,
    angler_map_y_coord_matcher_regex,
    non_number_replacement_regex
)
from ff14angler.dataClasses.comment.commentSection import CommentSection
from ff14angler.dataClasses.spot.gatheringTypeEnum import GatheringTypeEnum
from ff14angler.dataClasses.spot.spotCatchMetadata import SpotCatchMetadata
from ff14angler.dataClasses.spot.spotGatheringType import SpotGatheringType
from ff14angler.dataClasses.spot.spotId import SpotId
from ff14angler.network.xivapiWrapper import XivapiWrapper


@dataclass
class Spot(DataClassJsonMixin):
    spot_angler_area_id: Optional[int] = None
    spot_angler_catch_metadata: Optional[SpotCatchMetadata] = None
    spot_angler_comments: Optional[CommentSection] = None
    spot_angler_fishers_intuition_comment: Optional[str] = None
    spot_angler_gathering_level: Optional[int] = None
    spot_angler_name: Optional[str] = None
    spot_id: Optional[SpotId] = None
    # For some reason, `FishingSpot`s on xivapi use X and Z map coordinates and
    # angler uses X and Y map coordinates. I believe they both map to the in
    # game map's X and Z, but its possible angler's actually maps to some pixel
    # coordinate value on their map images for where they should place the
    # fishing hole.
    spot_angler_x_coord: Optional[int] = None
    spot_angler_y_coord: Optional[int] = None
    spot_angler_zone_name: Optional[str] = None
    spot_gathering_level: Optional[int] = None

    @staticmethod
    async def _parse_angler_area_id(spot_info: Tag) -> int:
        match = angler_map_area_matcher_regex.search(spot_info.find('a', {'class': None, 'rel': None}).attrs['href'])
        if match:
            return int(match.groups()[0])
        raise ValueError(f'Could not parse area from spot_info: {spot_info}')

    @staticmethod
    async def _parse_angler_fishers_intuition_comment(spot_info: Tag) -> Optional[str]:
        last_tr = spot_info.find_all('tr')[-1]
        if last_tr:
            for br_tag in last_tr.find_all('br'):  # type: Tag
                br_tag.replace_with('\n')
            return last_tr.text.strip() or None
        return None

    @staticmethod
    async def _parse_angler_x_coord(spot_info: Tag) -> int:
        match = angler_map_x_coord_matcher_regex.search(
            spot_info.find('a', {'class': None, 'rel': None}).attrs['href']
        )
        if match:
            return int(match.groups()[0])
        raise ValueError(f'Could not parse x coordinate from spot_info: {spot_info}')

    @staticmethod
    async def _parse_angler_y_coord(spot_info: Tag) -> int:
        match = angler_map_y_coord_matcher_regex.search(
            spot_info.find('a', {'class': None, 'rel': None}).attrs['href']
        )
        if match:
            return int(match.groups()[0])
        raise ValueError(f'Could not parse y coordinate from spot_info: {spot_info}')

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

        place_search_responses = await XivapiWrapper.xivapi_place_name_search(search_name)
        for place_search_response in place_search_responses:
            place_lookup_response = await XivapiWrapper.xivapi_place_name_lookup(place_search_response['ID'])
            fishing_spot = place_lookup_response['GameContentLinks'].get('FishingSpot')
            if fishing_spot and fishing_spot.get('PlaceName'):
                spot_lookup_response = await XivapiWrapper.xivapi_fishing_spot_lookup(
                    max(fishing_spot['PlaceName'])
                )

                self.spot_gathering_level = spot_lookup_response['GatheringLevel']
                self.spot_id.spot_gathering_type = SpotGatheringType.get_spot_gathering_type(
                    GatheringTypeEnum.RodFishing,
                    spot_lookup_response['ID']
                )

                return

        raise ValueError(f'Could not find fishing spot for spot: {self}')

    async def _lookup_spearfishing_ids_for_available_fish(self) -> Set[int]:
        if self.spot_angler_catch_metadata is None:
            raise ValueError(f'Cannot lookup available fish is spot_angler_catch_metadata is None: {self}')

        item_lookups = await asyncio.gather(
            *(
                XivapiWrapper.xivapi_item_lookup(
                    fish_id.fish_xivapi_item_id
                ) for fish_id in self.spot_angler_catch_metadata.spot_available_fish
            )
        )

        spearfishing_item_ids: Set[int] = set()
        for lookup in item_lookups:
            spearfishing_data: Dict[str, List[int]] = lookup['GameContentLinks'].get('SpearfishingItem')

            if spearfishing_data and len(spearfishing_data['Item']) == 1:
                spearfishing_item_ids.add(max(spearfishing_data['Item']))

        return spearfishing_item_ids

    async def update_spot_with_assume_is_teeming_spot(self):
        spearfishing_all_gpb = await XivapiWrapper.xivapi_spearfishing_gathering_point_base_index()
        current_spot_spearfishing_ids = await self._lookup_spearfishing_ids_for_available_fish()

        gpb_chance_assessment = []
        for gathering_point_base in spearfishing_all_gpb:
            gpb_chance_assessment.append(
                [
                    len(gathering_point_base['spearfishing_ids'].intersection(current_spot_spearfishing_ids)),
                    gathering_point_base
                ]
            )

        most_likely_gpb = max(gpb_chance_assessment, key=lambda x: x[0])
        if most_likely_gpb[0] == 0:
            # Filter out complete non matches
            raise ValueError(f'Could not find GatheringPointBase for spot: {self}')

        self.spot_gathering_level = most_likely_gpb[1]['gathering_point_base_level']
        self.spot_id.spot_gathering_type = SpotGatheringType.get_spot_gathering_type(
            GatheringTypeEnum.TeemingSpearFishing,
            most_likely_gpb[1]['gathering_point_base_id']
        )

    async def update_spot_with_assume_is_spearfishing_spot(self):
        if angler_spot_name_corrections.get(self.spot_angler_name):
            search_name: str = angler_spot_name_corrections.get(self.spot_angler_name)
        else:
            search_name: str = self.spot_angler_name

        place_search_responses = await XivapiWrapper.xivapi_place_name_search(search_name)

        for place_search_response in place_search_responses:
            place_lookup_response = await XivapiWrapper.xivapi_place_name_lookup(place_search_response['ID'])
            notebook = place_lookup_response['GameContentLinks'].get('SpearfishingNotebook')
            if notebook:
                spearfishing_ids: List[int] = notebook['PlaceName']

                if len(spearfishing_ids) != 1:
                    raise ValueError(f'Too many SpearfishingNotebook ids for spot! {self}')

                notebook_lookup = await XivapiWrapper.xivapi_spearfishing_notebook_lookup(max(spearfishing_ids))
                self.spot_gathering_level = notebook_lookup['GatheringLevel']
                self.spot_id.spot_gathering_type = SpotGatheringType.get_spot_gathering_type(
                    GatheringTypeEnum.SpearFishing,
                    notebook_lookup['ID']
                )
                return

        return await self.update_spot_with_assume_is_teeming_spot()

    async def update_spot_with_spot_soup(self, soup: BeautifulSoup) -> 'Spot':
        spot_info: Tag = soup.find('table', {'class': 'spot_info'})

        self.spot_angler_area_id = await self._parse_angler_area_id(spot_info)
        self.spot_angler_catch_metadata = await SpotCatchMetadata.get_spot_catch_metadata_from_spot_soup(soup)
        self.spot_angler_fishers_intuition_comment = await self._parse_angler_fishers_intuition_comment(spot_info)
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
