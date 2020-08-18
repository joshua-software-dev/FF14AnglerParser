#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Dict

from dataclasses_json import DataClassJsonMixin

from ff14angler.dataClasses.bait.bait import Bait
from ff14angler.dataClasses.fish.fish import Fish
from ff14angler.dataClasses.spot.spot import Spot


@dataclass
class ScrapingData(DataClassJsonMixin):
    bait: Dict[int, Bait]
    fish: Dict[int, Fish]
    spot: Dict[int, Spot]
