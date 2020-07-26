#! /usr/bin/env python3

from functools import cached_property
from dataclasses import dataclass
from typing import Dict

from bs4 import BeautifulSoup
from bs4.element import Tag


@dataclass
class WeatherPreferences:
    weathers: Dict[str, int] = None
    unique_catches_across_all_weathers: int = None

    @cached_property
    def weather_percentage(self) -> Dict[str, float]:
        return {k: v / self.unique_catches_across_all_weathers for k, v in self.weathers.items()}

    @classmethod
    def get_weather_preferences_from_soup(cls, soup: BeautifulSoup) -> 'WeatherPreferences':
        table: Tag = soup.find('table', {'class': 'info_section chart_weather'})
        tbody: Tag = table.find_all('tbody')[1]

        temp_weather: Dict[str, int] = dict()
        unique_catches = ''

        for tr in tbody.find_all('tr'):
            td1, td2 = tr.find_all('td')  # type: Tag, Tag
            cw_bar: Tag = td2.find('div', {'class': 'cw_bar'})
            weather_span: Tag = td1.find('span', {'class': 'weather_name'})

            weather_catches, unique_catches = cw_bar.attrs['title'].split('/')
            temp_weather[weather_span.text.strip()] = int(weather_catches)

        weather_preferences = cls()
        weather_preferences.weathers = temp_weather
        weather_preferences.unique_catches_across_all_weathers = int(unique_catches)

        return weather_preferences
