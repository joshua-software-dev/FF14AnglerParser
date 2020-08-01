#! /usr/bin/env python3

from dataclasses import dataclass

from ff14angler.dataClasses.bait.bait import Bait


@dataclass
class BaitPercentage:
    bait: Bait
    bait_percentage: str

    def __json__(self):
        return self.__dict__
