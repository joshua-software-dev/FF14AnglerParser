#! /usr/bin/env python3

import re

from dataclasses import dataclass

from bs4.element import Tag


@dataclass
class Leve:
    leve_item_angler_id: int = None
    leve_item_name: str = None
    leve_level: int = None
    leve_name: str = None
    leve_name_jp: str = None
    leve_turn_in_count: int = None

    def __json__(self):
        return self.__dict__

    @staticmethod
    def _parse_leve_name(td1: Tag) -> str:
        td1.find('font').decompose()
        if quest_text := td1.find('div'):
            quest_text.decompose()
        return td1.text.strip()

    @classmethod
    def get_leve_from_soup(cls, soup: Tag) -> 'Leve':
        td1, td2, td3, td4, _ = soup.find_all('td')  # type: Tag, Tag, Tag, Tag, _

        leve = cls()
        leve.leve_item_angler_id = int(td3.find('a').attrs['href'].split('/')[-1])
        leve.leve_item_name = td3.text.strip()
        leve.leve_level = td2.text.strip()
        leve.leve_name_jp = td1.find('font').text.strip()
        leve.leve_name = cls._parse_leve_name(td1)
        leve.leve_turn_in_count = int(re.sub(pattern=r"[^0-9]", repl='', string=td4.text))

        return leve
