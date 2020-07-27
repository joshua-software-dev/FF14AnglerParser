#! /usr/bin/env python3

from typing import Dict

from .fishData.bait import Bait


class BaitInfo:
    bait: Dict[str, Bait] = dict()

    @classmethod
    def __json__(cls):
        return cls.bait
