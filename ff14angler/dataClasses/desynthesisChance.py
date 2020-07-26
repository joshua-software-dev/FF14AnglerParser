#! /usr/bin/env python3

from dataclasses import dataclass

from bs4.element import Tag


@dataclass
class DesynthesisChance:
    desynthesis_icon: str = None
    desynthesis_lodestone_url: str = None
    desynthesis_name: str = None
    desynthesis_percentage: str = None

    def __json__(self):
        return self.__dict__

    @classmethod
    def get_desynthesis_chance_from_soup(cls, soup: Tag) -> 'DesynthesisChance':
        td1, td2, td3 = soup.find_all('td')  # type: Tag, Tag, Tag

        desynthesis_chance = cls()
        desynthesis_chance.desynthesis_icon = td2.find('img').attrs['src']
        desynthesis_chance.desynthesis_lodestone_url = td3.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href']
        desynthesis_chance.desynthesis_name = td2.text.strip()
        desynthesis_chance.desynthesis_percentage = td1.text.strip()

        return desynthesis_chance
