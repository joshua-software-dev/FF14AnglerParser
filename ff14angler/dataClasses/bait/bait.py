#! /usr/bin/env python3

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from bs4 import BeautifulSoup
from bs4.element import Tag

from ff14angler.aiohttpWrapped import AiohttpWrapped
from ff14angler.constants.data_corrections import (
    angler_bait_lodestone_url_corrections,
    angler_bait_missing_icon_urls,
    angler_bait_name_corrections
)
from ff14angler.constants.regex import non_number_replacement_regex
from ff14angler.dataClasses.bait.baitId import BaitId
from ff14angler.dataClasses.bait.baitAltCurrency import BaitAltCurrency
from ff14angler.dataClasses.comment.commentSection import CommentSection


@dataclass
class Bait:
    bait_id: BaitId
    bait_angler_name: str

    bait_alt_currency_prices: List[BaitAltCurrency] = field(default_factory=list)
    bait_angler_comments: Optional[CommentSection] = None
    bait_angler_large_icon_url: Optional[str] = None
    bait_angler_lodestone_url: Optional[str] = None
    bait_gil_cost: Optional[int] = None
    bait_gil_sell_price: Optional[int] = None
    bait_icon_url: Optional[str] = None
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
                shop_item_num: str = non_number_replacement_regex.sub(repl='', string=shop_item_label)
                shop_holder.add(
                    (
                        shop_response[f'ItemCost{shop_item_num}TargetID'],
                        shop_response[f'ItemCost{shop_item_num}']['Name_en'],
                        shop_response[f'CountCost{shop_item_num}'],
                    )
                )

        return [BaitAltCurrency(*shop) for shop in shop_holder]

    @staticmethod
    async def _parse_angler_large_icon_url(soup: BeautifulSoup) -> Optional[str]:
        partial_url: str = soup.find('div', {'class': 'clear_icon_l'}).find('img').attrs['src']
        if partial_url.endswith('0000.png'):
            return None
        return f'https://en.ff14angler.com{partial_url}'

    @staticmethod
    async def _parse_angler_lodestone_url(bait_id: BaitId, soup: BeautifulSoup) -> str:
        # noinspection SpellCheckingInspection
        lodestone_link: Tag = soup.find('a', {'class': 'lodestone eorzeadb_link'})
        if lodestone_link:
            return lodestone_link.attrs['href']
        elif angler_bait_lodestone_url_corrections.get(bait_id.bait_angler_bait_id):
            return angler_bait_lodestone_url_corrections.get(bait_id.bait_angler_bait_id)

        raise ValueError(f'Could not find lodestone link for bait: {bait_id}')

    @classmethod
    async def get_bait_from_angler_bait(cls, bait_angler_id: int, bait_angler_name: str):
        bait_id = await BaitId.get_bait_id_from_angler_bait(
            bait_angler_id=bait_angler_id,
            bait_angler_name=bait_angler_name
        )

        return cls(bait_id=bait_id, bait_angler_name=bait_angler_name)

    async def update_bait_with_assume_is_spearfishing_head(self):
        self.bait_icon_url = angler_bait_missing_icon_urls[self.bait_id.bait_angler_bait_id]
        self.bait_item_name = f'{self.bait_angler_name} Gig Head'
        self.bait_item_level = 61

    async def update_bait_with_bait_soup(self, soup: BeautifulSoup):
        if self.bait_angler_name in {'Small', 'Normal', 'Large'}:
            return await self.update_bait_with_assume_is_spearfishing_head()

        if corrected_name := angler_bait_name_corrections.get(self.bait_angler_name):
            search_name: str = corrected_name
        else:
            search_name: str = self.bait_angler_name

        search_response = await AiohttpWrapped.xivapi_item_search(search_name)
        lookup_response = await AiohttpWrapped.xivapi_item_lookup(search_response['ID'])

        self.bait_alt_currency_prices += await self._get_alt_currency_prices(
            lookup_response['GameContentLinks'].get('SpecialShop')
        )

        self.bait_angler_large_icon_url = await self._parse_angler_large_icon_url(soup)
        self.bait_angler_lodestone_url = await self._parse_angler_lodestone_url(self.bait_id, soup)
        self.bait_gil_cost: Optional[int] = lookup_response['PriceMid']
        self.bait_gil_sell_price: Optional[int] = lookup_response['PriceLow']
        self.bait_icon_url: Optional[str] = f'https://xivapi.com{lookup_response["Icon"]}'
        self.bait_item_level: Optional[int] = lookup_response['LevelItem']
        self.bait_item_name: Optional[str] = lookup_response['Name_en']

    async def update_bait_with_comment_section(self, comment_section: CommentSection):
        self.bait_angler_comments = comment_section
