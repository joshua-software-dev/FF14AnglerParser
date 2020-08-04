#! /usr/bin/env python3

from dataclasses import dataclass, field
from typing import List, Optional

from ff14angler.dataClasses.bait.baitId import BaitId
from ff14angler.dataClasses.fish.fishId import FishId
from ff14angler.dataClasses.spot.spotBaitFishCatchInfo import SpotBaitFishCatchInfo


@dataclass
class SpotBaitMetadata:
    spot_bait_id: BaitId

    spot_angler_bait_fish_catch_info: List[SpotBaitFishCatchInfo] = field(default_factory=list)
    spot_angler_bait_total_fish_caught: Optional[int] = None

    def __json__(self):
        return self.__dict__

    def update_spot_bait_metadata_with_spot_bait_fish_caught(
        self,
        caught_count: int,
        caught_percent: str,
        caught_total: int,
        fish_id: FishId
    ):
        if self.spot_angler_bait_total_fish_caught is not None:
            if self.spot_angler_bait_total_fish_caught != caught_total:
                raise ValueError('Got inconsistent total fish caught value.')

        self.spot_angler_bait_total_fish_caught = caught_total
        self.spot_angler_bait_fish_catch_info.append(
            SpotBaitFishCatchInfo(
                spot_angler_fish_caught_count=caught_count,
                spot_angler_fish_caught_percentage=caught_percent,
                spot_fish_id=fish_id
            )
        )
