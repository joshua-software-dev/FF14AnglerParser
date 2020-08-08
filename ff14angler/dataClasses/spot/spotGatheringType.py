#! /usr/bin/env python3

from dataclasses import dataclass

from typing import Optional

from ff14angler.dataClasses.spot.gatheringTypeEnum import GatheringTypeEnum


@dataclass
class SpotGatheringType:
    gathering_type: str
    gathering_type_unique_id: Optional[int] = None

    @classmethod
    def get_spot_gathering_type(
        cls,
        gathering_type: GatheringTypeEnum,
        unique_id: Optional[int] = None
    ) -> 'SpotGatheringType':
        return cls(gathering_type.value, unique_id)
