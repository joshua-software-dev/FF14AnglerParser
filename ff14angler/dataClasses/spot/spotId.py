#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from ff14angler.dataClasses.spot.spotGatheringType import SpotGatheringType


@dataclass_json
@dataclass
class SpotId:
    spot_angler_spot_id: int
    spot_gathering_type: Optional[SpotGatheringType] = None
