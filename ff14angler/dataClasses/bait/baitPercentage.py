#! /usr/bin/env python3

from dataclasses import dataclass

from ff14angler.dataClasses.bait.baitId import BaitId


@dataclass
class BaitPercentage:
    bait_id: BaitId
    bait_percentage: str

    @classmethod
    async def get_bait_percentage_from_export_json(cls, **kwargs):
        return cls(bait_id=BaitId(**kwargs['bait_id']), bait_percentage=kwargs['bait_percentage'])
