#! /usr/bin/env python3

import re

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from bs4 import BeautifulSoup
from bs4.element import Tag

from ff14angler.aiohttpWrapped import AiohttpWrapped
from ff14angler.dataClasses.bait.baitProvider import BaitPercentage, BaitProvider
from ff14angler.dataClasses.comment.comment import Comment
from ff14angler.dataClasses.fish.fishDesynthesisChance import FishDesynthesisChance
from ff14angler.dataClasses.fish.fishHourPreferences import FishHourPreferences
from ff14angler.dataClasses.fish.fishId import FishId
from ff14angler.dataClasses.fish.fishLeve import FishLeve
from ff14angler.dataClasses.fish.fishRecipe import FishRecipe
from ff14angler.dataClasses.fish.fishWeatherPreferences import FishWeatherPreferences
from ff14angler.dataClasses.spot.spot import Spot

if TYPE_CHECKING:
    # Avoiding circular imports
    from ff14angler.dataClasses.spot.spotProvider import Spot, SpotProvider


number_regex = re.compile(r"[^\d]")


@dataclass
class Fish:
    fish_angler_id: FishId
    fish_angler_name: str

    fish_angler_bait_preferences: List[BaitPercentage] = field(default_factory=list)
    fish_angler_canvas_size: Optional[str] = None
    fish_angler_comments: List[Comment] = field(default_factory=list)
    fish_angler_desynthesis_items: List[FishDesynthesisChance] = field(default_factory=list)
    fish_angler_double_hooking_count: Optional[str] = None
    fish_angler_gathering_spots: List[Spot] = field(default_factory=list)
    fish_angler_hour_preferences: Optional[FishHourPreferences] = None
    fish_angler_involved_leves: List[FishLeve] = field(default_factory=list)
    fish_angler_involved_recipes: List[FishRecipe] = field(default_factory=list)
    fish_angler_item_category: Optional[str] = None
    fish_angler_large_icon_url: Optional[str] = None
    fish_angler_lodestone_url: Optional[str] = None
    fish_angler_territory: Optional[str] = None
    fish_angler_weather_preferences: Optional[FishWeatherPreferences] = None
    fish_icon_url: Optional[str] = None
    fish_introduced_patch: Optional[str] = None
    fish_item_level: Optional[int] = None
    fish_item_name: Optional[str] = None
    fish_long_description: Optional[str] = None
    fish_short_description: Optional[str] = None

    def __json__(self):
        return self.__dict__

    @staticmethod
    async def _parse_angler_bait_preferences(soup: BeautifulSoup) -> List[BaitPercentage]:
        return await BaitProvider.get_bait_percentage_list_from_fish_soup(soup)

    @staticmethod
    async def _parse_angler_canvas_size(data_row3: Tag) -> Optional[str]:
        div_tag = data_row3.find('div', {'class': 'fancy info_icon_area'})
        if div_tag:
            a_tag = div_tag.find('a', {'class': 'clear_icon icon_with_text'})
            if a_tag:
                return a_tag.get('data-text')
        return None

    @staticmethod
    async def _parse_angler_comments(soup: BeautifulSoup) -> List[Comment]:
        return await Comment.get_comments_from_angler_comment_section_soup(soup)

    @staticmethod
    async def _parse_angler_desynthesis_items(soup: BeautifulSoup) -> List[FishDesynthesisChance]:
        """Not every fish has a desynthesis list."""
        # noinspection SpellCheckingInspection
        form = soup.find('form', {'name': 'desynthesized_delete'})
        temp_desynthesis_list: List[FishDesynthesisChance] = []

        if form:
            # noinspection SpellCheckingInspection
            if len(tbody := form.find_all('tbody')) > 1:
                for tag in tbody[1].find_all('tr'):  # type: Tag
                    temp_desynthesis_list.append(await FishDesynthesisChance.get_desynthesis_chance_from_soup(tag))

        return temp_desynthesis_list

    @staticmethod
    async def _parse_angler_double_hooking_count(data_row3: Tag) -> str:
        div_tag = data_row3.find('div', {'class': 'fancy info_icon_area'})
        span_tag = div_tag.find('span', {'class': 'clear_icon icon_with_text'})
        if span_tag:
            return span_tag.attrs.get('data-text')
        return '1'

    @staticmethod
    async def _parse_angler_gathering_spots(soup: BeautifulSoup) -> List[Spot]:
        # Avoiding circular imports
        from ff14angler.dataClasses.spot.spotProvider import Spot, SpotProvider

        temp_fishing_spot_list: List[Spot] = []

        spot_form = soup.find('form', {'name': 'spot_delete'})
        if spot_form:
            angler_zone_name: str = ''
            # noinspection SpellCheckingInspection
            body = spot_form.find_all('tbody')[1]

            for tag in body.find_all('tr'):  # type: Tag
                if not tag.find('a'):
                    angler_zone_name = tag.text.strip()
                    continue

                td1, _, td3 = tag.find_all('td')  # type: Tag, _, Tag
                spot = await SpotProvider.get_spot_from_angler_spot(
                    int(number_regex.sub(repl='', string=td1.find('a').attrs['href'])),
                    td1.text.strip(),
                    angler_zone_name
                )
                temp_fishing_spot_list.append(spot)

        return temp_fishing_spot_list

    @staticmethod
    async def _parse_angler_hour_preferences(soup: BeautifulSoup) -> Optional[FishHourPreferences]:
        return await FishHourPreferences.get_hour_preferences_from_fish_soup(soup)

    @staticmethod
    async def _parse_angler_involved_leves(soup: BeautifulSoup) -> List[FishLeve]:
        """Not every fish is used as a leve turn in."""
        header = soup.find('h3', {'id': 'leve'})
        temp_leve_list: List[FishLeve] = []

        if header:
            table: Tag = header.find_next('table', {'class': 'list'})
            if table:
                for tag in table.find_all('tr'):  # type: Tag
                    temp_leve_list.append(await FishLeve.get_leve_from_soup(tag))

        return temp_leve_list

    @staticmethod
    async def _parse_angler_involved_recipes(soup: BeautifulSoup) -> List[FishRecipe]:
        """Not every fish is an ingredient in a recipe."""
        # noinspection SpellCheckingInspection
        header = soup.find('h3', {'id': 'receipe'})
        temp_recipe_list: List[FishRecipe] = []

        if header:
            table: Tag = header.find_next('table', {'class': 'list'})
            if table:
                for tag in table.find_all('tr'):  # type: Tag
                    temp_recipe_list.append(await FishRecipe.get_recipe_from_fish_soup(tag))

        return temp_recipe_list

    @staticmethod
    async def _parse_angler_item_category(data_row2: Tag) -> str:
        span1, _, _ = data_row2.find_all('span')  # type: Tag, _, _
        return span1.text.strip()

    @staticmethod
    async def _parse_angler_large_icon_url(data_row1: Tag) -> str:
        div_tag = data_row1.find('div', {'class': 'clear_icon_l'})
        img_tag = div_tag.find('img')
        return 'https://en.ff14angler.com{}'.format(img_tag.attrs['src'])

    @staticmethod
    async def _parse_angler_lodestone_url(data_row2: Tag) -> Optional[str]:
        # noinspection SpellCheckingInspection
        a_tag = data_row2.find('a', {'class', 'lodestone eorzeadb_link'})
        if a_tag:
            return a_tag.attrs['href']
        return None

    @staticmethod
    async def _parse_angler_territory(data_row2: Tag) -> Optional[str]:
        _, span2, _ = data_row2.find_all('span')  # type: _, Tag, _
        territory = ' '.join(span2.text.strip().split()[1:])
        if territory:
            return territory
        return None

    @staticmethod
    async def _parse_angler_weather_preferences(soup: BeautifulSoup) -> Optional[FishWeatherPreferences]:
        return await FishWeatherPreferences.get_weather_preferences_from_fish_soup(soup)

    @staticmethod
    async def _parse_icon_url(data_row1: Tag) -> str:
        div_tag = data_row1.find('div', {'class': 'clear_icon_l'})
        img_tag = div_tag.find('img')
        return 'https://en.ff14angler.com{}'.format(img_tag.attrs['src'].replace('l.png', '.png'))

    @staticmethod
    async def _parse_fish_introduced_patch(data_row2: Tag) -> str:
        return data_row2.find('span', {'class': 'patch'}).attrs['patch']

    async def _lookup_fish_introduced_patch(self, data_row2: Tag, item_lookup_response: Dict[str, Any]) -> str:
        try:
            return item_lookup_response['GamePatch']['Version']  # type: str
        except KeyError:
            return await self._parse_fish_introduced_patch(data_row2)

    @staticmethod
    async def _parse_item_level(data_row2: Tag) -> int:
        _, span2, _ = data_row2.find_all('span')  # type: _, Tag, _
        return int(span2.text.strip().split()[0])

    @staticmethod
    async def _lookup_fish_long_description(item_lookup_response: Dict[str, Any]) -> Optional[str]:
        game_content_links: Dict[str, Any] = item_lookup_response['GameContentLinks']

        try:
            fish_lookup_response = await AiohttpWrapped.xivapi_fish_parameter_lookup(
                game_content_links['FishParameter']['Item'][0]
            )
            return fish_lookup_response['Text_en']  # type: str
        except KeyError:
            try:
                fish_lookup_response = await AiohttpWrapped.xivapi_spearfishing_item_lookup(
                    game_content_links['SpearfishingItem']['Item'][0]
                )
                return fish_lookup_response['Description_en']  # type: str
            except KeyError:
                return None

    async def update_fish_with_fish_soup(self, soup: BeautifulSoup) -> 'Fish':
        search_response = await AiohttpWrapped.xivapi_item_search(self.fish_angler_name)
        item_lookup_response = await AiohttpWrapped.xivapi_item_lookup(search_response['ID'])
        fish_table: Tag = soup.find('table', {'class': 'fish_info'})

        # noinspection SpellCheckingInspection
        if ranking := fish_table.find('span', {'class': 'ranklist note frame'}):
            ranking.decompose()

        data_row1, data_row2, data_row3 = fish_table.find_all('tr')[:3]  # type: Tag, Tag, Tag

        self.fish_angler_bait_preferences += await self._parse_angler_bait_preferences(soup)
        self.fish_angler_canvas_size = await self._parse_angler_canvas_size(data_row3)
        self.fish_angler_comments += await self._parse_angler_comments(soup)
        self.fish_angler_desynthesis_items += await self._parse_angler_desynthesis_items(soup)
        self.fish_angler_double_hooking_count = await self._parse_angler_double_hooking_count(data_row3)
        self.fish_angler_gathering_spots += await self._parse_angler_gathering_spots(soup)
        self.fish_angler_hour_preferences = await self._parse_angler_hour_preferences(soup)
        self.fish_angler_involved_leves += await self._parse_angler_involved_leves(soup)
        self.fish_angler_involved_recipes += await self._parse_angler_involved_recipes(soup)
        self.fish_angler_item_category = await self._parse_angler_item_category(data_row2)
        self.fish_angler_large_icon_url = await self._parse_angler_large_icon_url(data_row1)
        self.fish_angler_lodestone_url = await self._parse_angler_lodestone_url(data_row2)
        self.fish_angler_territory = await self._parse_angler_territory(data_row2)
        self.fish_angler_weather_preferences = await self._parse_angler_weather_preferences(soup)
        self.fish_icon_url = f'https://xivapi.com{item_lookup_response["Icon"]}'
        self.fish_introduced_patch = await self._lookup_fish_introduced_patch(data_row2, item_lookup_response)
        self.fish_item_level = await self._parse_item_level(data_row2)
        self.fish_item_name = item_lookup_response['Name_en']
        self.fish_long_description = await self._lookup_fish_long_description(item_lookup_response)
        self.fish_short_description = item_lookup_response['Description_en']

        return self

    @classmethod
    async def get_fish_from_angler_fish(cls, fish_angler_id: int, fish_angler_name: str):
        fish_id = await FishId.get_fish_id_from_angler_fish(
            fish_angler_id=fish_angler_id,
            fish_angler_name=fish_angler_name
        )

        return cls(fish_id, fish_angler_name)