#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Set


# noinspection SpellCheckingInspection
angler_bait_blacklisted_bait_id: Set[int] = {
    318  # Coerthan Crab is mislabelled as a bait
}

angler_bait_lodestone_url_corrections: Dict[int, str] = {
    1082: 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/ba252ebbdd9/'
}

angler_bait_missing_icon_urls: Dict[int, str] = {
    2001: '/i/060000/060671.png',
    2002: '/i/060000/060672.png',
    2003: '/i/060000/060673.png',
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

spot_territory_correction: Dict[str, str] = {
    'Domanische Enklave': 'Yanxia',
    'The Doman Enclave': 'Yanxia',
    'Quartier enclavé de Doma': 'Yanxia',
    'ドマ町人地': 'ヤンサ',

    'Diadem-Grotte': 'Das Diadem',
    'Diadem Grotto': 'The Diadem',
    'Grotte du Diadème': 'Le Diadème',
    'ディアデム諸島の洞穴': 'ディアデム諸島',

    'Südlicher Diademteich': 'Das Diadem',
    'Southern Diadem Lake': 'The Diadem',
    'Mares du quadrant sud-ouest': 'Le Diadème',
    'ディアデム諸島の南西池': 'ディアデム諸島',

    'Nördlicher Diademteich': 'Das Diadem',
    'Northern Diadem Lake': 'The Diadem',
    'Étang du quadrant nord-ouest': 'Le Diadème',
    'ディアデム諸島の北西池': 'ディアデム諸島',

    'Tosende Wolken': 'Das Diadem',
    'Blustery Cloudtop': 'The Diadem',
    'Cimes venteuses': 'Le Diadème',
    '風吹き抜ける雲海': 'ディアデム諸島',

    'Sanfte Wolken': 'Das Diadem',
    'Calm Cloudtop': 'The Diadem',
    'Cimes calmes': 'Le Diadème',
    '風穏やかな雲海': 'ディアデム諸島',

    'Wirbelnde Wolken': 'Das Diadem',
    'Swirling Cloudtop': 'The Diadem',
    'Cimes tumultueuses': 'Le Diadème',
    '風渦巻く雲海': 'ディアデム諸島',

    'Sturmumtostes Wolkenmeer': 'Das Diadem',
    'Windswept Cloudtop': 'The Diadem',
    'Cimes éventées': 'Le Diadème',
    '風吹き上がる雲海': 'ディアデム諸島',
}
