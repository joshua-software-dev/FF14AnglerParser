#! /usr/bin/env python3

import re

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Set

from bs4.element import Tag

from .baitAltCurrency import BaitAltCurrency
from ...aiohttpWrapped import AiohttpWrapped


number_regex = re.compile(r"[^\d]")


@dataclass
class BaitData:
    bait_alt_currency_prices: List[BaitAltCurrency]
    bait_angler_bait_id: Optional[int]
    bait_angler_name: str
    bait_gil_cost: int
    bait_gil_sell_price: int
    bait_icon_url: str
    bait_item_id: int
    bait_item_name: str
    bait_level: int

    bait_angler_large_icon_url: Optional[str] = None
    bait_angler_lodestone_url: Optional[str] = None
    bait_angler_percentage: Optional[str] = None

    def __json__(self):
        return self.__dict__

    @classmethod
    async def _get_alt_currency_info(cls, lookup_response: Dict[str, Any]) -> List[BaitAltCurrency]:
        shop_holder: Set[Tuple[int, str, int]] = set()
        special_shops: Optional[Dict[str, List[int]]] = lookup_response['GameContentLinks'].get('SpecialShop')

        if special_shops is not None:
            for shop_item_label, shop_list in special_shops.items():
                shop_response = await AiohttpWrapped.xivapi_special_shop_lookup(shop_list[0])
                shop_item_num: str = number_regex.sub(repl='', string=shop_item_label)
                shop_holder.add(
                    (
                        shop_response[f'ItemCost{shop_item_num}TargetID'],
                        shop_response[f'ItemCost{shop_item_num}']['Name_en'],
                        shop_response[f'CountCost{shop_item_num}'],
                    )
                )

        return [BaitAltCurrency(*shop) for shop in shop_holder]

    async def update_bait_with_bait_soup(self) -> 'BaitData':
        """Fill in additional data about bait with angler bait page soup."""
        raise NotImplementedError

    async def update_bait_with_fish_soup(self, td1: Tag, td2: Tag, td4: Tag) -> 'BaitData':
        """Fill in additional data about bait with angler fish page soup."""
        if self.bait_angler_bait_id is None:
            self.bait_angler_bait_id = int(re.sub(r"[^0-9]", '', td2.find('a').attrs['href']))

        self.bait_angler_large_icon_url = 'https://en.ff14angler.com{}'.format(
            td2.find('img').attrs['src'].replace('.png', 'l.png')
        )

        # noinspection SpellCheckingInspection
        self.bait_angler_lodestone_url = td4.find('a', {'class': 'lodestone eorzeadb_link'}).attrs['href']
        self.bait_angler_percentage = td1.text.strip()

        return self

    @classmethod
    async def get_bait_from_angler_name(cls, angler_bait_name: str, angler_bait_id: int = None) -> 'BaitData':
        # noinspection SpellCheckingInspection
        name_corrections: Dict[str, str] = {
            'fistful of northern krill': 'northern krill',
            'pot of salmon roe': 'salmon roe',
            'strip of jerked ovim': 'jerked ovim',
            'box of baitbugs': 'baitbugs'
        }

        search_response = await AiohttpWrapped.xivapi_item_search(
            name_corrections.get(angler_bait_name) or angler_bait_name
        )
        lookup_response = await AiohttpWrapped.xivapi_item_lookup(search_response['ID'])

        return cls(
            bait_alt_currency_prices=await cls._get_alt_currency_info(lookup_response),
            bait_angler_bait_id=angler_bait_id,
            bait_angler_name=angler_bait_name,
            bait_gil_cost=lookup_response['PriceMid'],
            bait_gil_sell_price=lookup_response['PriceLow'],
            bait_icon_url=f'https://xivapi.com{lookup_response["Icon"]}',
            bait_item_id=lookup_response['ID'],
            bait_item_name=lookup_response['Name_en'],
            bait_level=lookup_response['LevelItem']
        )
