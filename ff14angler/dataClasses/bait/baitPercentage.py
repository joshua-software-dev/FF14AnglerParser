#! /usr/bin/env python3

from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin

from ff14angler.dataClasses.bait.baitId import BaitId


@dataclass
class BaitPercentage(DataClassJsonMixin):
    bait_id: BaitId
    bait_percentage: str
