#! /usr/bin/env python3

from functools import cached_property
from dataclasses import dataclass
from typing import Dict

from bs4 import BeautifulSoup
from bs4.element import Tag


@dataclass
class WeatherPreferences:
    weathers: Dict[str, int]
    unique_catches_across_all_weathers: int

    def __json__(self):
        _temp = self.__dict__
        _temp['weather_percentage'] = self.weather_percentage
        return _temp

    @cached_property
    def weather_percentage(self) -> Dict[str, float]:
        return {k: v / self.unique_catches_across_all_weathers for k, v in self.weathers.items()}

    @staticmethod
    async def _parse_weathers(weather_table: Tag) -> Dict[str, int]:
        temp_weather: Dict[str, int] = dict()
        # noinspection SpellCheckingInspection
        tbody: Tag = weather_table.find_all('tbody')[1]

        for tr in tbody.find_all('tr'):
            td1, td2 = tr.find_all('td')  # type: Tag, Tag
            weather_name: str = td1.find('span', {'class': 'weather_name'}).text.strip()
            cw_bar: Tag = td2.find('div', {'class': 'cw_bar'})

            weather_catches: int = int(cw_bar.attrs['title'].split('/')[0])
            temp_weather[weather_name] = weather_catches

        return temp_weather

    @staticmethod
    async def _parse_unique_catches_across_all_weathers(weather_table: Tag) -> int:
        num_holder = weather_table.find('span', {'class': 'small'})
        return int(num_holder.find('b').text.strip())

    @classmethod
    async def get_weather_preferences_from_soup(cls, soup: BeautifulSoup) -> 'WeatherPreferences':
        weather_table: Tag = soup.find('table', {'class': 'info_section chart_weather'})

        return cls(
            weathers=await cls._parse_weathers(weather_table),
            unique_catches_across_all_weathers=await cls._parse_unique_catches_across_all_weathers(weather_table)
        )
