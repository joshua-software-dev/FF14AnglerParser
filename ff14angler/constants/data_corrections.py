#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import Dict, Set


angler_bait_lodestone_url_corrections: Dict[int, str] = {
    1082: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/ba252ebbdd9/'
}

angler_bait_missing_icon_urls: Dict[int, str] = {
    2001: 'https://xivapi.com/i/060000/060671.png',
    2002: 'https://xivapi.com/i/060000/060672.png',
    2003: 'https://xivapi.com/i/060000/060673.png'
}

# noinspection SpellCheckingInspection
angler_bait_name_corrections: Dict[str, str] = {
    'fistful of northern krill': 'northern krill',
    'pot of salmon roe': 'salmon roe',
    'strip of jerked ovim': 'jerked ovim',
    'box of baitbugs': 'baitbugs'
}

angler_bait_name_do_not_search: Set[str] = {'Small', 'Normal', 'Large'}

# noinspection SpellCheckingInspection
angler_desynthesis_item_name_corrections: Dict[str, str] = {
    'ドライハイエーテル': 'Dried Hi-Ether',
    '達識のエクスマテリジャ': "Gatherer's Guerdon Materia VIII",
    'Waterproof Cotton': 'Waterproof Cotton Cloth'
}

angler_fish_lodestone_url_corrections: Dict[int, str] = {
    3086: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/564719300e5',
    3299: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/77c295edae2/',
    3300: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/a3de98862e0/'
}

# noinspection SpellCheckingInspection
angler_spot_name_corrections: Dict[str, str] = {'SuinoSato': 'Sui–no–Sato'}
