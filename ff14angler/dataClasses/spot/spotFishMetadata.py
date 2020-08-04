#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, List, Union

from ff14angler.dataClasses.fish.fishId import FishId


@dataclass
class SpotFishMetadata:
    spot_fish_id: FishId
    spot_angler_fish_tug_strength: List[Dict[str, Union[float, int]]]

    def __json__(self):
        return self.__dict__

    @classmethod
    async def get_spot_fish_metadata(cls, fish_id: FishId, tug_strength: Dict[str, float]) -> 'SpotFishMetadata':
        return cls(
            spot_fish_id=fish_id,
            spot_angler_fish_tug_strength=[
                {
                    'tug_strength': int(strength_num),
                    'tug_strength_percent': strength_percent
                } for strength_num, strength_percent in tug_strength.items()
            ]
        )
