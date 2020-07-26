#! /usr/bin/env python3

from functools import cached_property
from dataclasses import dataclass
from typing import Dict, List

from bs4 import BeautifulSoup
from bs4.element import Tag


@dataclass
class HourPreferences:
    hours: Dict[int, int] = None
    unique_catches_across_all_hours: int = None

    @cached_property
    def hours_percentage(self) -> Dict[int, float]:
        return {k: v / self.unique_catches_across_all_hours for k, v in self.hours.items()}

    @classmethod
    def get_hour_preferences_from_soup(cls, soup: BeautifulSoup) -> 'HourPreferences':
        time_table: Tag = soup.find('table', {'class': 'info_section timezone'})
        hours: List[Tag] = time_table.find_all('td', {'class': 'tz_hour'})

        temp_hour_list: Dict[int, int] = dict()
        unique_catches = ''

        for hour in hours:
            hour_div = hour.find('div')
            hour_label = hour.find('label')

            hour_catches, unique_catches = hour_div.attrs['title'].split('/')
            temp_hour_list[int(hour_label.text.strip())] = int(hour_catches)

        hour_preferences = cls()
        hour_preferences.hours = {k: v for k, v in sorted(temp_hour_list.items(), key=lambda x: x[0])}
        hour_preferences.unique_catches_across_all_hours = int(unique_catches)

        return hour_preferences
