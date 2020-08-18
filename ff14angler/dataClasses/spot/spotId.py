#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Optional

from dataclasses_json import DataClassJsonMixin

from ff14angler.dataClasses.spot.spotGatheringType import SpotGatheringType


@dataclass
class SpotId(DataClassJsonMixin):
    spot_angler_spot_id: int
    spot_gathering_type: Optional[SpotGatheringType] = None
