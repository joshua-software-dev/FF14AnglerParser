#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Optional

from ff14angler.dataClasses.spot.spotGatheringType import SpotGatheringType


@dataclass
class SpotId:
    spot_angler_spot_id: int
    spot_gathering_type: Optional[SpotGatheringType] = None

    @classmethod
    async def get_spot_id_from_export_json(cls, **kwargs):
        return cls(
            spot_angler_spot_id=kwargs['spot_angler_spot_id'],
            spot_gathering_type=SpotGatheringType(**kwargs['spot_gathering_type'])
        )
