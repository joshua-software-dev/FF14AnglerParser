#! /usr/bin/env python3

from dataclasses import dataclass

from bs4.element import Tag


@dataclass
class DesynthesisChance:
    desynthesis_icon_url: str
    desynthesis_lodestone_url: str
    desynthesis_name: str
    desynthesis_percentage: str

    def __json__(self):
        return self.__dict__

    @classmethod
    def get_desynthesis_chance_from_soup(cls, soup: Tag) -> 'DesynthesisChance':
        td1, td2, td3 = soup.find_all('td')  # type: Tag, Tag, Tag

        return cls(
            desynthesis_icon_url=td2.find('img').attrs['src'],
            desynthesis_lodestone_url=td3.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href'],
            desynthesis_name=td2.text.strip(),
            desynthesis_percentage=td1.text.strip()
        )
