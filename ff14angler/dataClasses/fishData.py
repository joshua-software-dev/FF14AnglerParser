#! /usr/bin/env python3

import re

from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

from .bait import Bait
from .comment import Comment
from .desynthesisChance import DesynthesisChance
from .fishingHole import FishingHole
from .hourPreferences import HourPreferences
from .leve import Leve
from .recipe import Recipe
from .weatherPreferences import WeatherPreferences


@dataclass
class FishData:
    angler_id: int = None
    canvas_size: str = None
    double_hooking_count: str = None
    fish_item_category: str = None
    fish_item_level: int = None
    fish_name: str = None
    fish_territory: str = None
    icon_url: str = None
    large_icon_url: str = None
    lodestone_url: str = None
    long_description: str = None
    patch: str = None
    short_description: str = None

    fishing_holes: List[FishingHole] = None

    hour_preferences: HourPreferences = None

    weather_preferences: WeatherPreferences = None

    bait_preferences: List[Bait] = None

    comment_list: List[Comment] = None

    desynthesis_list: List[DesynthesisChance] = None

    recipe_list: List[Recipe] = None

    leve_list: List[Leve] = None

    def __json__(self):
        return self.__dict__

    @staticmethod
    def _parse_angler_id(data_row1: Tag) -> int:
        span_tag = data_row1.find('span', {'class': 'toggle_timetable'})
        return int(span_tag.attrs['data-fish'])

    @staticmethod
    def _parse_canvas_size(data_row3: Tag) -> str:
        div_tag = data_row3.find('div', {'class': 'fancy info_icon_area'})
        a_tag = div_tag.find('a', {'class': 'clear_icon icon_with_text'})
        return a_tag.attrs['data-text']

    @staticmethod
    def _parse_double_hooking_count(data_row3: Tag) -> str:
        div_tag = data_row3.find('div', {'class': 'fancy info_icon_area'})
        span_tag = div_tag.find('span', {'class': 'clear_icon icon_with_text'})
        return span_tag.attrs['data-text']

    @staticmethod
    def _parse_fish_item_category(data_row2: Tag) -> str:
        span1, _, _ = data_row2.find_all('span')  # type: Tag, _, _
        return span1.text.strip()

    @staticmethod
    def _parse_fish_item_level(data_row2: Tag) -> int:
        _, span2, _ = data_row2.find_all('span')  # type: _, Tag, _
        item_level, _ = span2.text.strip().split()
        return int(item_level)

    @staticmethod
    def _parse_fish_name(data_row1: Tag) -> str:
        span_tag = data_row1.find('span', {'class': 'name'})
        return span_tag.text.strip()

    @staticmethod
    def _parse_fish_territory(data_row2: Tag) -> str:
        _, span2, _ = data_row2.find_all('span')  # type: _, Tag, _
        _, territory = span2.text.strip().split()
        return territory

    @staticmethod
    def _parse_icon_url(data_row1: Tag) -> str:
        div_tag = data_row1.find('div', {'class': 'clear_icon_l'})
        img_tag = div_tag.find('img')
        return img_tag.attrs['src']

    @staticmethod
    def _parse_lodestone_url(data_row2: Tag) -> str:
        a_tag = data_row2.find('a', {'class', re.compile('lodestone')})
        return a_tag.attrs['href']

    @staticmethod
    def _parse_long_description(data_row5: Tag) -> str:
        for tag in data_row5.find_all('br'):
            tag.replace_with('\n')

        return data_row5.text.strip()

    @staticmethod
    def _parse_patch(data_row2: Tag) -> str:
        _, _, span3 = data_row2.find_all('span')  # type: _, Tag, _
        return span3.attrs['patch']

    @staticmethod
    def _parse_short_description(data_row3: Tag) -> str:
        for tag in data_row3.find_all('br'):
            tag.replace_with('\n')

        return data_row3.text.strip()

    @staticmethod
    def _parse_fishing_holes(soup: BeautifulSoup) -> List[FishingHole]:
        location_table = soup.find('form', {'name': 'spot_delete'})
        body = location_table.find_all('tbody')[1]
        temp_fishing_hole_list: List[FishingHole] = []

        for tag in body.find_all('tr'):  # type: Tag
            if tag.find('a'):
                fishing_hole = FishingHole.get_fishing_hole_from_soup(tag)
                temp_fishing_hole_list.append(fishing_hole)

        return temp_fishing_hole_list

    @staticmethod
    def _parse_hour_preferences(soup: BeautifulSoup) -> HourPreferences:
        return HourPreferences.get_hour_preferences_from_soup(soup)

    @staticmethod
    def _parse_weather_preferences(soup: BeautifulSoup) -> WeatherPreferences:
        return WeatherPreferences.get_weather_preferences_from_soup(soup)

    @staticmethod
    def _parse_bait_preferences(soup: BeautifulSoup) -> List[Bait]:
        temp_bait: List[Bait] = []

        for tr in soup.find_all('tr', {'class': 'bait'}):  # type: Tag
            bait = Bait.get_bait_from_soup(tr)
            temp_bait.append(bait)

        return temp_bait

    @staticmethod
    def _parse_comment_list(soup: BeautifulSoup) -> List[Comment]:
        comment_container: Tag = soup.find('div', {'class': 'comment_list'})
        comment_list_soup: List[Tag] = comment_container.find_all('div', {'class': 'comment'})

        temp_comment_list: List[Comment] = []

        for comment in comment_list_soup:

            temp_comment_list.append(Comment.get_comment_from_soup(comment))

        return temp_comment_list

    @staticmethod
    def _parse_desynthesis_chance_from_soup(soup: BeautifulSoup) -> List[DesynthesisChance]:
        """Not every fish has a desynthesis list."""
        form = soup.find('form', {'name': 'desynthesized_delete'})
        temp_desynthesis_list: List[DesynthesisChance] = []

        if form:
            if len(tbody := form.find_all('tbody')) > 1:
                for tag in tbody[1].find_all('tr'):  # type: Tag
                    temp_desynthesis_list.append(DesynthesisChance.get_desynthesis_chance_from_soup(tag))

        return temp_desynthesis_list

    @staticmethod
    def _parse_recipe_ingredient_list(soup: BeautifulSoup):
        """Not every fish is an ingredient in a recipe."""
        header = soup.find('h3', {'id': 'receipe'})
        temp_recipe_list: List[Recipe] = []

        if header:
            table: Tag = header.find_next('table', {'class': 'list'})
            if table:
                for tag in table.find_all('tr'):  # type: Tag
                    temp_recipe_list.append(Recipe.get_recipe_from_soup(tag))

        return temp_recipe_list

    @staticmethod
    def _parse_leve_turn_in_list(soup: BeautifulSoup):
        """Not every fish is used as a leve turn in."""
        header = soup.find('h3', {'id': 'leve'})
        temp_leve_list: List[Leve] = []

        if header:
            table: Tag = header.find_next('table', {'class': 'list'})
            if table:
                for tag in table.find_all('tr'):  # type: Tag
                    temp_leve_list.append(Leve.get_leve_from_soup(tag))

        return temp_leve_list

    @classmethod
    def get_fish_data_from_soup(cls, soup: BeautifulSoup) -> 'FishData':
        fish_table: Tag = soup.find('table', {'class': 'fish_info'})

        if ranking := fish_table.find('span', {'class': 'ranklist note frame'}):
            ranking.decompose()

        data_row1, data_row2, data_row3, _, data_row5 = fish_table.find_all('tr')  # type: Tag, Tag, Tag, _, Tag

        fish_data = cls()
        fish_data.angler_id = cls._parse_angler_id(data_row1)
        fish_data.canvas_size = cls._parse_canvas_size(data_row3)
        fish_data.double_hooking_count = cls._parse_double_hooking_count(data_row3)
        fish_data.fish_item_category = cls._parse_fish_item_category(data_row2)
        fish_data.fish_item_level = cls._parse_fish_item_level(data_row2)
        fish_data.fish_name = cls._parse_fish_name(data_row1)
        fish_data.fish_territory = cls._parse_fish_territory(data_row2)
        fish_data.large_icon_url = cls._parse_icon_url(data_row1)
        fish_data.icon_url = fish_data.large_icon_url.replace('l.png', '.png')
        fish_data.lodestone_url = cls._parse_lodestone_url(data_row2)
        fish_data.long_description = cls._parse_long_description(data_row5)
        fish_data.patch = cls._parse_patch(data_row2)
        fish_data.short_description = cls._parse_short_description(data_row3)

        fish_data.fishing_holes = cls._parse_fishing_holes(soup)

        fish_data.hour_preferences = cls._parse_hour_preferences(soup)

        fish_data.weather_preferences = cls._parse_weather_preferences(soup)

        fish_data.bait_preferences = cls._parse_bait_preferences(soup)

        fish_data.comment_list = cls._parse_comment_list(soup)

        fish_data.desynthesis_list = cls._parse_desynthesis_chance_from_soup(soup)

        fish_data.recipe_list = cls._parse_recipe_ingredient_list(soup)

        fish_data.leve_list = cls._parse_leve_turn_in_list(soup)

        return fish_data
