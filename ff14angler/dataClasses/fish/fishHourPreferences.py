#! /usr/bin/env python3

from functools import cached_property
from dataclasses import dataclass
from typing import Dict, Optional

from bs4 import BeautifulSoup  # type: ignore
from bs4.element import Tag  # type: ignore


@dataclass
class FishHourPreferences:
    hours: Dict[int, int]
    unique_catches_across_all_hours: int

    def __json__(self):
        _temp = self.__dict__
        _temp['hours_percentage'] = self.hours_percentage
        return _temp

    @cached_property
    def hours_percentage(self) -> Dict[int, float]:
        return {k: v / self.unique_catches_across_all_hours for k, v in self.hours.items()}

    @staticmethod
    async def _parse_hours(time_table: Tag) -> Dict[int, int]:
        temp_hours: Dict[int, int] = dict()

        for hour in time_table.find_all('td', {'class': 'tz_hour'}):  # type: Tag
            hour_div = hour.find('div', {'class': 'tz_bar'})
            if hour_div:
                hour_catches: int = int(hour_div.attrs['title'].split('/')[0])
            else:
                hour_catches = 0
            hour_label: int = int(hour.find('label').text.strip())
            temp_hours[hour_label] = hour_catches

        return {k: v for k, v in sorted(temp_hours.items(), key=lambda x: x[0])}

    @staticmethod
    async def _parse_unique_catches_across_all_hours(time_table: Tag) -> int:
        num_holder = time_table.find('span', {'class': 'small'})
        return int(num_holder.find('b').text.strip())

    @classmethod
    async def get_hour_preferences_from_fish_soup(cls, soup: BeautifulSoup) -> Optional['FishHourPreferences']:
        time_table: Tag = soup.find('table', {'class': 'info_section timezone'})

        if not time_table:
            return None

        return cls(
            hours=await cls._parse_hours(time_table),
            unique_catches_across_all_hours=await cls._parse_unique_catches_across_all_hours(time_table)
        )
