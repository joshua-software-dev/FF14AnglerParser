#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Dict

from bs4.element import Tag


@dataclass
class Recipe:
    recipe_crafter: str = None
    recipe_icon: str = None
    recipe_lodestone_url: str = None
    recipe_name: str = None

    def __json__(self):
        return self.__dict__

    @staticmethod
    def _parse_crafter(td2: Tag) -> str:
        _lookup: Dict[str, str] = {
            '/img/i_relavant001.png': 'CRP',
            '/img/i_relavant002.png': 'BSM',
            '/img/i_relavant003.png': 'ARM',
            '/img/i_relavant004.png': 'GSM',
            '/img/i_relavant005.png': 'LTW',
            # There is no weaver image for some reason
            '/img/i_relavant007.png': 'ALC',
            '/img/i_relavant008.png': 'CUL'
        }

        return _lookup[td2.find('img').attrs['src']]

    @classmethod
    def get_recipe_from_soup(cls, soup: Tag) -> 'Recipe':
        td1, td2, td3, td4 = soup.find_all('td')  # type: Tag, Tag, Tag, Tag

        recipe = cls()
        recipe.recipe_crafter = cls._parse_crafter(td2)
        recipe.recipe_icon = td1.find('img').attrs['src']
        recipe.recipe_lodestone_url = td4.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href']
        recipe.recipe_name = td3.text.strip()

        return recipe
