#! /usr/bin/env python3

from dataclasses import dataclass

from dataclasses_json import dataclass_json

from ff14angler.dataClasses.bait.baitId import BaitId


@dataclass_json
@dataclass
class BaitPercentage:
    bait_id: BaitId
    bait_percentage: str
