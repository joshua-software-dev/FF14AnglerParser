#! /usr/bin/env python3


class XivApi:
    cached_responses = dict()

    cached_responses.setdefault('FishParameter', dict())
    cached_responses.setdefault('FishingSpot', dict())
    cached_responses.setdefault('Item', dict())
    cached_responses.setdefault('Leve', dict())
    cached_responses.setdefault('PlaceName', dict())
    cached_responses.setdefault('SpearfishingItem', dict())
    cached_responses.setdefault('SpecialShop', dict())
    cached_responses.setdefault(
        'Search',
        {
            'Item': dict(),
            'Leve': dict(),
            'PlaceName': dict()
        }
    )
