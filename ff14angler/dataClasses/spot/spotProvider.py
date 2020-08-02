#! /usr/bin/env python3

from typing import Dict

from ff14angler.dataClasses.spot.spot import Spot
from ff14angler.dataClasses.spot.spotId import SpotId


class SpotProvider:
    spot_holder: Dict[int, Spot] = dict()

    @classmethod
    def __json__(cls):
        return cls.spot_holder

    @classmethod
    async def get_spot_from_angler_spot(
        cls,
        spot_angler_id: int,
        spot_angler_name: str,
        spot_angler_zone_name: str
    ) -> Spot:
        if result := cls.spot_holder.get(spot_angler_id):
            return result

        cls.spot_holder[spot_angler_id] = Spot(
            spot_angler_spot_id=spot_angler_id,
            spot_angler_name=spot_angler_name,
            spot_angler_zone_name=spot_angler_zone_name
        )

        return cls.spot_holder[spot_angler_id]

    @classmethod
    async def get_spot_id_from_angler_id(cls, spot_angler_id: int) -> SpotId:
        spot = cls.spot_holder[spot_angler_id]
        return SpotId(spot_angler_spot_id=spot.spot_angler_spot_id, spot_gathering_type=spot.spot_gathering_type)
