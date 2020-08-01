#! /usr/bin/env python3

import re

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from bs4 import BeautifulSoup
from bs4.element import Tag

from ff14angler.aiohttpWrapped import AiohttpWrapped
from ff14angler.dataClasses.bait.baitAltCurrency import BaitAltCurrency
from ff14angler.dataClasses.comment.comment import Comment


# noinspection SpellCheckingInspection
name_corrections: Dict[str, str] = {
    'fistful of northern krill': 'northern krill',
    'pot of salmon roe': 'salmon roe',
    'strip of jerked ovim': 'jerked ovim',
    'box of baitbugs': 'baitbugs'
}
number_regex = re.compile(r"[^\d]")


@dataclass
class Bait:
    bait_angler_id: int
    bait_angler_name: str

    bait_alt_currency_prices: List[BaitAltCurrency] = field(default_factory=list)
    bait_angler_comments: List[Comment] = field(default_factory=list)
    bait_angler_large_icon_url: Optional[str] = None
    bait_angler_lodestone_url: Optional[str] = None
    bait_gil_cost: Optional[int] = None
    bait_gil_sell_price: Optional[int] = None
    bait_icon_url: Optional[str] = None
    bait_item_id: Optional[int] = None
    bait_item_level: Optional[int] = None
    bait_item_name: Optional[str] = None

    def __json__(self):
        return self.__dict__

    @staticmethod
    async def _get_alt_currency_prices(special_shops: Optional[Dict[str, List[int]]]) -> List[BaitAltCurrency]:
        shop_holder: Set[Tuple[int, str, int]] = set()

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

    @staticmethod
    async def _parse_angler_comments(soup: BeautifulSoup) -> List[Comment]:
        return await Comment.get_comments_from_angler_comment_section_soup(soup)

    @staticmethod
    async def _parse_angler_large_icon_url(soup: BeautifulSoup) -> str:
        partial_url: str = soup.find('div', {'class': 'clear_icon_l'}).find('img').attrs['src']
        return f'https://en.ff14angler.com{partial_url}'

    @staticmethod
    async def _parse_angler_lodestone_url(soup: BeautifulSoup) -> Optional[str]:
        # noinspection SpellCheckingInspection
        lodestone_link: Tag = soup.find('a', {'class': 'lodestone eorzeadb_link'})
        if lodestone_link:
            return lodestone_link.attrs['href']
        return None

    async def update_bait_with_assume_is_spearfishing_head(self, soup: BeautifulSoup):
        self.bait_angler_comments = await self._parse_angler_comments(soup)
        self.bait_item_name = f'{self.bait_angler_name} Gig Head'

    async def update_bait_with_bait_soup(self, soup: BeautifulSoup):
        if self.bait_angler_name in {'Small', 'Normal', 'Large'}:
            return await self.update_bait_with_assume_is_spearfishing_head(soup)

        if corrected_name := name_corrections.get(self.bait_angler_name):
            search_name: str = corrected_name
        else:
            search_name: str = self.bait_angler_name

        search_response = await AiohttpWrapped.xivapi_item_search(search_name)
        lookup_response = await AiohttpWrapped.xivapi_item_lookup(search_response['ID'])

        self.bait_alt_currency_prices += await self._get_alt_currency_prices(
            lookup_response['GameContentLinks'].get('SpecialShop')
        )

        self.bait_angler_comments = await self._parse_angler_comments(soup)
        self.bait_angler_large_icon_url = await self._parse_angler_large_icon_url(soup)
        self.bait_angler_lodestone_url = await self._parse_angler_lodestone_url(soup)
        self.bait_gil_cost: Optional[int] = lookup_response['PriceMid']
        self.bait_gil_sell_price: Optional[int] = lookup_response['PriceLow']
        self.bait_icon_url: Optional[str] = f'https://xivapi.com{lookup_response["Icon"]}'
        self.bait_item_id: Optional[int] = lookup_response['ID']
        self.bait_item_level: Optional[int] = lookup_response['LevelItem']
        self.bait_item_name: Optional[str] = lookup_response['Name_en']
