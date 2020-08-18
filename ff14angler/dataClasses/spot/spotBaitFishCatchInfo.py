#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from ff14angler.dataClasses.fish.fishId import FishId


@dataclass_json
@dataclass
class SpotBaitFishCatchInfo:
    spot_angler_fish_caught_count: int
    spot_angler_fish_caught_percentage: str
    spot_fish_id: FishId

    spot_angler_fish_average_seconds_to_hook: Optional[int] = None
