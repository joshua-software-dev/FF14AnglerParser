#! /usr/bin/env python3

from typing import Dict, TypedDict

from ff14angler.dataClasses.bait.bait import Bait
from ff14angler.dataClasses.fish.fish import Fish
from ff14angler.dataClasses.spot.spot import Spot


HomePageData = TypedDict('HomePageData', {'bait': Dict[int, Bait], 'fish': Dict[int, Fish], 'spot': Dict[int, Spot]})
