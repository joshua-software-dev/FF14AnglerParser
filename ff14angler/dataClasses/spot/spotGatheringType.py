#! /usr/bin/env python3

from dataclasses import dataclass

from typing import Optional, Union


gathering_type_index = {
    0: 'FishingSpot',
    1: 'GatheringPointBase',
    2: 'SpearfishingNotebook',
    'rod': 'FishingSpot',
    'teeming': 'GatheringPointBase',
    'spear': 'SpearfishingNotebook'
}


@dataclass
class SpotGatheringType:
    gathering_type: str
    gathering_type_unique_id: Optional[int] = None

    def __json__(self):
        return self.__dict__

    @classmethod
    def get_spot_gathering_type(
        cls,
        gathering_type: Union[int, str],
        unique_id: Optional[int] = None
    ) -> 'SpotGatheringType':
        return cls(gathering_type_index[gathering_type], unique_id)
