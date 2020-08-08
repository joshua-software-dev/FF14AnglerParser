#! /usr/bin/env python3

from dataclasses import dataclass

from ff14angler.dataClasses.bait.baitId import BaitId


@dataclass
class BaitPercentage:
    bait_id: BaitId
    bait_percentage: str
