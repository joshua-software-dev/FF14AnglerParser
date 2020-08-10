#! /usr/bin/env python3

import json

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup  # type: ignore
from bs4.element import Tag  # type: ignore

from ff14angler.constants.regex import angler_bait_metadata_catch_count_regex, non_number_replacement_regex
from ff14angler.dataClasses.bait.baitId import BaitId
from ff14angler.dataClasses.bait.baitProvider import BaitProvider
from ff14angler.dataClasses.fish.fishProvider import FishProvider
from ff14angler.dataClasses.fish.fishId import FishId
from ff14angler.dataClasses.spot.spotBaitMetadata import SpotBaitMetadata


@dataclass
class SpotCatchMetadata:
    spot_available_fish: List[FishId] = field(default_factory=list)
    spot_effective_bait: List[BaitId] = field(default_factory=list)
    spot_fish_caught_per_bait: List[SpotBaitMetadata] = field(default_factory=list)

    @staticmethod
    async def _parse_angler_available_fish_from_spot_soup(soup: BeautifulSoup) -> List[FishId]:
        temp_fish_list: List[FishId] = []
        form = soup.find('form', {'name': 'spot_delete'})
        # noinspection SpellCheckingInspection
        body = form.find_all('tbody')[1]

        for tag in body.find_all('tr'):  # type: Tag
            tds = tag.find_all('td')
            td2: Tag = tds[1]
            td4: Tag = tds[3]

            fish_angler_id: int = int(non_number_replacement_regex.sub(repl='', string=td2.find('a').attrs['href']))
            fish_angler_name: str = td2.text.strip()
            fish = await FishProvider.get_fish_from_angler_fish(fish_angler_id, fish_angler_name)

            tug_canvas = td4.find('canvas')
            if tug_canvas:
                canvas_data: str = tug_canvas.attrs['data-value']
            else:
                canvas_data = '{}'

            temp_fish_list.append(fish.fish_id)
            await fish.update_fish_with_tug_strength(json.loads(canvas_data))

        return temp_fish_list

    @staticmethod
    async def _parse_angler_effective_bait_from_spot_soup(soup: BeautifulSoup) -> Dict[int, BaitId]:
        temp_bait_map: Dict[int, BaitId] = dict()
        table = soup.find('table', {'id': 'effective_bait'})
        for row_num, row in enumerate(table.find_all('tr')):  # type: int, Tag
            if row_num == 0:
                continue
            img_holder = row.select('.clear_icon')
            if img_holder:
                bait_angler_id: int = int(
                    non_number_replacement_regex.sub(
                        repl='',
                        string=img_holder[0].find('img').attrs['src']
                    )
                )

                try:
                    bait = BaitProvider.bait_holder[bait_angler_id]
                except KeyError:
                    bait_angler_name: str = img_holder[0].attrs['title']
                    bait = await BaitProvider.get_bait_from_angler_bait(bait_angler_id, bait_angler_name)
                    await bait.update_bait_with_assume_is_mooch_fish()

                temp_bait_map[bait.bait_id.bait_angler_bait_id] = bait.bait_id

        return temp_bait_map

    @classmethod
    async def _parse_spot_bait_metadata_average_time_to_catch(
        cls,
        spot_bait_metadata_map: Dict[int, SpotBaitMetadata],
        soup: BeautifulSoup
    ) -> List[SpotBaitMetadata]:
        # noinspection SpellCheckingInspection
        for td in soup.find_all('td', {'class': 'hooktime'}):  # type: Tag
            bait_angler_id: int = int(
                non_number_replacement_regex.sub(
                    repl='',
                    string=td.find('a', {'class': 'clear_icon'}).attrs['href']
                )
            )

            bait = spot_bait_metadata_map[bait_angler_id]

            # noinspection SpellCheckingInspection
            for a_tag in td.find_all('a', {'rsec': True}):  # type: Tag
                fish_angler_id: int = int(non_number_replacement_regex.sub(repl='', string=a_tag.attrs['href']))
                for fish_info in bait.spot_angler_bait_fish_catch_info:
                    if fish_info.spot_fish_id.fish_angler_fish_id == fish_angler_id:
                        # noinspection SpellCheckingInspection
                        fish_info.spot_angler_fish_average_seconds_to_hook = int(a_tag.attrs['rsec'])
                        break

        return list(spot_bait_metadata_map.values())

    @staticmethod
    async def _parse_caught_count_caught_total(data: str) -> Tuple[int, int]:
        match = angler_bait_metadata_catch_count_regex.search(data)
        if match:
            caught_count, caught_total = match.groups()  # type: str, str
            return int(caught_count), int(caught_total)
        raise ValueError(f'Could not parse spot caught count total: {data}')

    @classmethod
    async def _parse_spot_bait_metadata(
        cls,
        available_fish: List[FishId],
        effective_bait: Dict[int, BaitId],
        soup: BeautifulSoup
    ) -> List[SpotBaitMetadata]:
        spot_bait_metadata_map: Dict[int, SpotBaitMetadata] = dict()
        table = soup.find('table', {'id': 'effective_bait'})
        for row_num, row in enumerate(table.find_all('tr')):  # type: int, Tag
            if row_num == 0:
                continue
            for cell_num, cell in enumerate(row.find_all('td')):
                if cell_num == 0:
                    bait_img = row.select('.clear_icon')[0].find('img')
                    bait_angler_id: int = int(non_number_replacement_regex.sub(repl='', string=bait_img.attrs['src']))
                    bait_metadata = SpotBaitMetadata(effective_bait[bait_angler_id])
                    spot_bait_metadata_map[bait_angler_id] = bait_metadata
                    continue

                fish_rate = cell.find('div', {'class': 'fish_rate clear_icon'})
                if fish_rate:
                    if float(fish_rate.find('canvas').attrs['value']) <= 0:
                        continue
                    data: str = fish_rate.attrs['title'].split()[-1]
                    caught_count, caught_total = await cls._parse_caught_count_caught_total(data)
                    caught_percent: str = data.replace(f'({caught_count}/{caught_total})', '').strip()

                    # noinspection PyUnboundLocalVariable
                    bait_metadata.update_spot_bait_metadata_with_spot_bait_fish_caught(
                        caught_count,
                        caught_percent,
                        caught_total,
                        available_fish[cell_num - 1]
                    )

        return await cls._parse_spot_bait_metadata_average_time_to_catch(spot_bait_metadata_map, soup)

    @classmethod
    async def get_spot_catch_metadata_from_export_json(cls, **kwargs) -> 'SpotCatchMetadata':
        return cls(
            spot_available_fish=[FishId(**fish_id) for fish_id in kwargs['spot_available_fish']],
            spot_effective_bait=[BaitId(**bait_id) for bait_id in kwargs['spot_effective_bait']],
            spot_fish_caught_per_bait=[
                await SpotBaitMetadata.get_spot_bait_metadata_from_export_json(
                    **caught
                ) for caught in kwargs['spot_fish_caught_per_bait']
            ]
        )

    @classmethod
    async def get_spot_catch_metadata_from_spot_soup(cls, soup: BeautifulSoup):
        available_fish = await cls._parse_angler_available_fish_from_spot_soup(soup)
        effective_bait = await cls._parse_angler_effective_bait_from_spot_soup(soup)

        return cls(
            spot_available_fish=available_fish,
            spot_effective_bait=list(effective_bait.values()),
            spot_fish_caught_per_bait=await cls._parse_spot_bait_metadata(available_fish, effective_bait, soup)
        )
