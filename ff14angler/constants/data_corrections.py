#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import Dict, Set


angler_bait_lodestone_url_corrections: Dict[int, str] = {
    1082: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/ba252ebbdd9/'
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
    3299: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/77c295edae2/',
    3300: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/a3de98862e0/'
}

# noinspection SpellCheckingInspection
angler_spot_name_corrections: Dict[str, str] = {'SuinoSato': 'Sui–no–Sato'}
