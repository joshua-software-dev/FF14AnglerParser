#! /usr/bin/env python3

from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from .comment import Comment
from .desynthesisChance import DesynthesisChance
from .fishingHole import FishingHole
from .hourPreferences import HourPreferences
from .leve import Leve
from .recipe import Recipe
from .weatherPreferences import WeatherPreferences
from ..baitData import BaitData, BaitProvider
from ...aiohttpWrapped import AiohttpWrapped


@dataclass
class FishData:
    fish_data_icon_url: str
    fish_data_level: int
    fish_data_long_description: Optional[str]
    fish_data_patch: Optional[str]
    fish_data_short_description: str
    fish_data_item_id: int
    fish_data_item_name: str

    fish_data_angler_comments: List[Comment] = field(default_factory=list)
    fish_data_angler_fish_id: Optional[int] = None
    fish_data_angler_fish_item_category: Optional[str] = None
    fish_data_angler_fish_name: Optional[str] = None
    fish_data_angler_bait_preferences: List[BaitData] = field(default_factory=list)
    fish_data_angler_canvas_size: Optional[str] = None
    fish_data_angler_desynthesis_items: List[DesynthesisChance] = field(default_factory=list)
    fish_data_angler_double_hooking_count: Optional[str] = None
    fish_data_angler_fishing_holes: List[FishingHole] = field(default_factory=list)
    fish_data_angler_hour_preferences: Optional[HourPreferences] = None
    fish_data_angler_involved_leves: List[Leve] = field(default_factory=list)
    fish_data_angler_involved_recipes: List[Recipe] = field(default_factory=list)
    fish_data_angler_large_icon_url: Optional[str] = None
    fish_data_angler_lodestone_url: Optional[str] = None
    fish_data_angler_territory: Optional[str] = None
    fish_data_angler_weather_preferences: Optional[WeatherPreferences] = None

    def __json__(self):
        return self.__dict__

    @staticmethod
    async def _parse_angler_comments(soup: BeautifulSoup) -> List[Comment]:
        comment_container: Tag = soup.find('div', {'class': 'comment_list'})
        comment_list_soup: List[Tag] = comment_container.find_all('div', {'class': 'comment'})

        temp_comment_list: Set[Comment] = set()

        for soup_comment in comment_list_soup:

            temp_comment_list.add(await Comment.get_comment_from_soup(soup_comment))

        return [c for c in sorted(temp_comment_list, key=lambda x: x.comment_timestamp)]

    @staticmethod
    async def _parse_angler_fish_id(data_row1: Tag) -> int:
        span_tag = data_row1.find('span', {'class': 'toggle_timetable'})
        return int(span_tag.attrs['data-fish'])

    @staticmethod
    async def _parse_angler_fish_item_category(data_row2: Tag) -> str:
        span1, _, _ = data_row2.find_all('span')  # type: Tag, _, _
        return span1.text.strip()

    @staticmethod
    async def parse_angler_fish_name(data_row1: Tag) -> str:
        span_tag = data_row1.find('span', {'class': 'name'})
        return span_tag.text.strip()

    @staticmethod
    async def _parse_angler_bait_preferences(soup: BeautifulSoup) -> List[BaitData]:
        return await BaitProvider.get_bait_data_list_from_fish_soup(soup)

    @staticmethod
    async def _parse_angler_canvas_size(data_row3: Tag) -> str:
        div_tag = data_row3.find('div', {'class': 'fancy info_icon_area'})
        a_tag = div_tag.find('a', {'class': 'clear_icon icon_with_text'})
        return a_tag.attrs['data-text']

    @staticmethod
    async def _parse_angler_desynthesis_items(soup: BeautifulSoup) -> List[DesynthesisChance]:
        """Not every fish has a desynthesis list."""
        # noinspection SpellCheckingInspection
        form = soup.find('form', {'name': 'desynthesized_delete'})
        temp_desynthesis_list: List[DesynthesisChance] = []

        if form:
            # noinspection SpellCheckingInspection
            if len(tbody := form.find_all('tbody')) > 1:
                for tag in tbody[1].find_all('tr'):  # type: Tag
                    temp_desynthesis_list.append(await DesynthesisChance.get_desynthesis_chance_from_soup(tag))

        return temp_desynthesis_list

    @staticmethod
    async def _parse_angler_double_hooking_count(data_row3: Tag) -> str:
        div_tag = data_row3.find('div', {'class': 'fancy info_icon_area'})
        span_tag = div_tag.find('span', {'class': 'clear_icon icon_with_text'})
        return span_tag.attrs['data-text']

    @staticmethod
    async def _parse_angler_fishing_holes(soup: BeautifulSoup) -> List[FishingHole]:
        location_table = soup.find('form', {'name': 'spot_delete'})
        # noinspection SpellCheckingInspection
        body = location_table.find_all('tbody')[1]
        temp_fishing_hole_list: List[FishingHole] = []

        for tag in body.find_all('tr'):  # type: Tag
            if tag.find('a'):
                temp_fishing_hole_list.append(await FishingHole.get_fishing_hole_from_soup(tag))

        return temp_fishing_hole_list

    @staticmethod
    async def _parse_angler_hour_preferences(soup: BeautifulSoup) -> HourPreferences:
        return await HourPreferences.get_hour_preferences_from_soup(soup)

    @staticmethod
    async def _parse_icon_url(data_row1: Tag) -> str:
        div_tag = data_row1.find('div', {'class': 'clear_icon_l'})
        img_tag = div_tag.find('img')
        return 'https://en.ff14angler.com{}'.format(img_tag.attrs['src'].replace('l.png', '.png'))

    @staticmethod
    async def _parse_angler_involved_leves(soup: BeautifulSoup):
        """Not every fish is used as a leve turn in."""
        header = soup.find('h3', {'id': 'leve'})
        temp_leve_list: List[Leve] = []

        if header:
            table: Tag = header.find_next('table', {'class': 'list'})
            if table:
                for tag in table.find_all('tr'):  # type: Tag
                    temp_leve_list.append(await Leve.get_leve_from_soup(tag))

        return temp_leve_list

    @staticmethod
    async def _parse_angler_involved_recipes(soup: BeautifulSoup):
        """Not every fish is an ingredient in a recipe."""
        # noinspection SpellCheckingInspection
        header = soup.find('h3', {'id': 'receipe'})
        temp_recipe_list: List[Recipe] = []

        if header:
            table: Tag = header.find_next('table', {'class': 'list'})
            if table:
                for tag in table.find_all('tr'):  # type: Tag
                    temp_recipe_list.append(await Recipe.get_recipe_from_soup(tag))

        return temp_recipe_list

    @staticmethod
    async def _parse_angler_large_icon_url(data_row1: Tag) -> str:
        div_tag = data_row1.find('div', {'class': 'clear_icon_l'})
        img_tag = div_tag.find('img')
        return 'https://en.ff14angler.com{}'.format(img_tag.attrs['src'])

    @staticmethod
    async def _parse_fish_level(data_row2: Tag) -> int:
        _, span2, _ = data_row2.find_all('span')  # type: _, Tag, _
        item_level, _ = span2.text.strip().split()
        return int(item_level)

    @staticmethod
    async def _parse_angler_lodestone_url(data_row2: Tag) -> str:
        # noinspection SpellCheckingInspection
        a_tag = data_row2.find('a', {'class', 'lodestone eorzeadb_link'})
        return a_tag.attrs['href']

    @staticmethod
    async def _read_xivapi_long_description(item_lookup_response: Dict[str, Any]) -> Optional[str]:
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

    @staticmethod
    async def _parse_long_description(data_row5: Tag) -> str:
        for tag in data_row5.find_all('br'):
            tag.replace_with('\n')

        return data_row5.text.strip()

    @staticmethod
    async def _read_xivapi_fish_introduced_patch(item_lookup_response: dict) -> Optional[str]:
        try:
            return item_lookup_response['GamePatch']['Version']  # type: str
        except KeyError:
            return None

    @staticmethod
    async def _parse_fish_introduced_patch(data_row2: Tag) -> str:
        _, _, span3 = data_row2.find_all('span')  # type: _, Tag, _
        return span3.attrs['patch']

    @staticmethod
    async def _parse_short_description(data_row3: Tag) -> str:
        for tag in data_row3.find_all('br'):
            tag.replace_with('\n')

        return data_row3.text.strip()

    @staticmethod
    async def _parse_angler_fish_territory(data_row2: Tag) -> str:
        _, span2, _ = data_row2.find_all('span')  # type: _, Tag, _
        _, territory = span2.text.strip().split()
        return territory

    @staticmethod
    async def _parse_angler_weather_preferences(soup: BeautifulSoup) -> WeatherPreferences:
        return await WeatherPreferences.get_weather_preferences_from_soup(soup)

    async def update_fish_data_from_fish_soup(self, soup: BeautifulSoup) -> 'FishData':
        fish_table: Tag = soup.find('table', {'class': 'fish_info'})

        # noinspection SpellCheckingInspection
        if ranking := fish_table.find('span', {'class': 'ranklist note frame'}):
            ranking.decompose()

        data_row1, data_row2, data_row3, _, data_row5 = fish_table.find_all('tr')  # type: Tag, Tag, Tag, _, Tag

        if self.fish_data_patch is None:
            self.fish_data_patch = await self._parse_fish_introduced_patch(data_row2)

        self.fish_data_angler_comments += await self._parse_angler_comments(soup)
        self.fish_data_angler_fish_id = await self._parse_angler_fish_id(data_row1)
        self.fish_data_angler_fish_item_category = await self._parse_angler_fish_item_category(data_row2)
        self.fish_data_angler_fish_name = await self.parse_angler_fish_name(data_row1)
        self.fish_data_angler_bait_preferences += await self._parse_angler_bait_preferences(soup)
        self.fish_data_angler_canvas_size = await self._parse_angler_canvas_size(data_row3)
        self.fish_data_angler_desynthesis_items += await self._parse_angler_desynthesis_items(soup)
        self.fish_data_angler_double_hooking_count = await self._parse_angler_double_hooking_count(data_row3)
        self.fish_data_angler_fishing_holes += await self._parse_angler_fishing_holes(soup)
        self.fish_data_angler_hour_preferences = await self._parse_angler_hour_preferences(soup)
        self.fish_data_angler_involved_leves += await self._parse_angler_involved_leves(soup)
        self.fish_data_angler_involved_recipes += await self._parse_angler_involved_recipes(soup)
        self.fish_data_angler_large_icon_url = await self._parse_angler_large_icon_url(data_row1)
        self.fish_data_angler_lodestone_url = await self._parse_angler_lodestone_url(data_row2)
        self.fish_data_angler_territory = await self._parse_angler_fish_territory(data_row2)
        self.fish_data_angler_weather_preferences = await self._parse_angler_weather_preferences(soup)

        return self

    @classmethod
    async def get_fish_data_from_fish_soup(cls, soup: BeautifulSoup) -> 'FishData':
        fish_table: Tag = soup.find('table', {'class': 'fish_info'})

        # noinspection SpellCheckingInspection
        if ranking := fish_table.find('span', {'class': 'ranklist note frame'}):
            ranking.decompose()

        data_row1, data_row2, data_row3, _, data_row5 = fish_table.find_all('tr')  # type: Tag, Tag, Tag, _, Tag
        angler_fish_name: str = await cls.parse_angler_fish_name(data_row1)

        response = await AiohttpWrapped.xivapi_item_search(angler_fish_name)
        item_id: int = response['ID']
        item_name: str = response['Name']

        if item_id is None or item_name is None:
            raise ValueError(f'Could not find xivapi item for item: {angler_fish_name}')

        return cls(
            fish_data_angler_bait_preferences=await cls._parse_angler_bait_preferences(soup),
            fish_data_angler_canvas_size=await cls._parse_angler_canvas_size(data_row3),
            fish_data_angler_comments=await cls._parse_angler_comments(soup),
            fish_data_angler_desynthesis_items=await cls._parse_angler_desynthesis_items(soup),
            fish_data_angler_double_hooking_count=await cls._parse_angler_double_hooking_count(data_row3),
            fish_data_angler_fish_id=await cls._parse_angler_fish_id(data_row1),
            fish_data_angler_fish_item_category=await cls._parse_angler_fish_item_category(data_row2),
            fish_data_angler_fish_name=angler_fish_name,
            fish_data_angler_fishing_holes=await cls._parse_angler_fishing_holes(soup),
            fish_data_angler_hour_preferences=await cls._parse_angler_hour_preferences(soup),
            fish_data_angler_involved_leves=await cls._parse_angler_involved_leves(soup),
            fish_data_angler_involved_recipes=await cls._parse_angler_involved_recipes(soup),
            fish_data_angler_large_icon_url=await cls._parse_angler_large_icon_url(data_row1),
            fish_data_angler_lodestone_url=await cls._parse_angler_lodestone_url(data_row2),
            fish_data_angler_territory=await cls._parse_angler_fish_territory(data_row2),
            fish_data_angler_weather_preferences=await cls._parse_angler_weather_preferences(soup),
            fish_data_icon_url=await cls._parse_icon_url(data_row1),
            fish_data_item_id=item_id,
            fish_data_item_name=item_name,
            fish_data_level=await cls._parse_fish_level(data_row2),
            fish_data_long_description=await cls._parse_long_description(data_row5),
            fish_data_patch=await cls._parse_fish_introduced_patch(data_row2),
            fish_data_short_description=await cls._parse_short_description(data_row3)
        )

    @classmethod
    async def get_fish_data_from_angler_name(cls, angler_fish_name: str, angler_fish_id: int = None) -> 'FishData':
        search_response = await AiohttpWrapped.xivapi_item_search(angler_fish_name)
        fish_data_xivapi_item_id: int = search_response['ID']
        fish_data_xivapi_item_name: str = search_response['Name']

        if fish_data_xivapi_item_id is None or fish_data_xivapi_item_name is None:
            print(angler_fish_name)
            print(search_response)
            raise ValueError('Fish ID/Name cannot be None')

        item_lookup_response = await AiohttpWrapped.xivapi_item_lookup(fish_data_xivapi_item_id)
        fish_data_icon_url: str = f'https://xivapi.com{item_lookup_response["Icon"]}'
        fish_data_level: int = item_lookup_response['LevelItem']
        fish_data_short_description: str = item_lookup_response['Description_en']

        fish_data_patch: Optional[str] = await cls._read_xivapi_fish_introduced_patch(item_lookup_response)
        fish_data_long_description: Optional[str] = await cls._read_xivapi_long_description(item_lookup_response)

        return cls(
            fish_data_icon_url=fish_data_icon_url,
            fish_data_level=fish_data_level,
            fish_data_long_description=fish_data_long_description,
            fish_data_patch=fish_data_patch,
            fish_data_short_description=fish_data_short_description,
            fish_data_item_id=fish_data_xivapi_item_id,
            fish_data_item_name=fish_data_xivapi_item_name,
            fish_data_angler_fish_id=angler_fish_id
        )
