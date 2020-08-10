#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Optional

from ff14angler.dataClasses.fish.fishId import FishId


@dataclass
class SpotBaitFishCatchInfo:
    spot_angler_fish_caught_count: int
    spot_angler_fish_caught_percentage: str
    spot_fish_id: FishId

    spot_angler_fish_average_seconds_to_hook: Optional[int] = None

    @classmethod
    async def get_spot_bait_fish_catch_info_from_export_json(cls, **kwargs):
        return cls(
            **{
                **kwargs,
                **{'spot_fish_id': FishId(**kwargs['spot_fish_id'])}
            }
        )
