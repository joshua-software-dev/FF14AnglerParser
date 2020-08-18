#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse

from typing import Dict, Set

from ff14angler.constants.values import ANGLER_API_BASE_URL


angler_bait_blacklisted_bait_id: Set[int] = {
    318  # Coerthan Crab is mislabelled as a bait
}

angler_bait_lodestone_url_corrections: Dict[int, str] = {
    1082: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/ba252ebbdd9/'
}

angler_bait_missing_icon_urls: Dict[int, str] = {
    2001: urllib.parse.urljoin(ANGLER_API_BASE_URL, 'i/060000/060671.png'),
    2002: urllib.parse.urljoin(ANGLER_API_BASE_URL, 'i/060000/060672.png'),
    2003: urllib.parse.urljoin(ANGLER_API_BASE_URL, 'i/060000/060673.png'),
}

# noinspection SpellCheckingInspection
angler_bait_name_corrections: Dict[str, str] = {
    'fistful of northern krill': 'northern krill',
    'pot of salmon roe': 'salmon roe',
    'strip of jerked ovim': 'jerked ovim',
    'box of baitbugs': 'baitbugs'
}

angler_bait_name_do_not_search: Set[str] = {'Small', 'Normal', 'Large'}

angler_desynthesis_item_name_corrections: Dict[str, str] = {
    'Waterproof Cotton': 'Waterproof Cotton Cloth'
}

angler_fish_lodestone_url_corrections: Dict[int, str] = {
    3086: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/564719300e5',
    3299: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/77c295edae2/',
    3300: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/a3de98862e0/'
}

# noinspection SpellCheckingInspection
angler_spot_name_corrections: Dict[str, str] = {'SuinoSato': 'Sui–no–Sato'}
