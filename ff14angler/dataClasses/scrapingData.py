#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Dict

from dataclasses_json import dataclass_json

from ff14angler.dataClasses.bait.bait import Bait
from ff14angler.dataClasses.fish.fish import Fish
from ff14angler.dataClasses.spot.spot import Spot


@dataclass_json
@dataclass
class ScrapingData:
    bait: Dict[int, Bait]
    fish: Dict[int, Fish]
    spot: Dict[int, Spot]
