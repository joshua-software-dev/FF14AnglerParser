#! /usr/bin/env python3

from dataclasses import dataclass

from ff14angler.dataClasses.spot.spotGatheringType import SpotGatheringType


@dataclass
class SpotId:
    spot_angler_spot_id: int
    spot_gathering_type: SpotGatheringType

    def __json__(self):
        return self.__dict__