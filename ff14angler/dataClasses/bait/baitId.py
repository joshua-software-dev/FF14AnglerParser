#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Optional

from dataclasses_json import DataClassJsonMixin

from ff14angler.constants.data_corrections import angler_bait_name_corrections, angler_bait_name_do_not_search
from ff14angler.network.xivapiWrapper import XivapiWrapper


@dataclass
class BaitId(DataClassJsonMixin):
    bait_angler_bait_id: int
    bait_xivapi_item_id: Optional[int]

    @classmethod
    async def get_bait_id_from_angler_bait(cls, bait_angler_id: int, bait_angler_name: str):
        if bait_angler_name in angler_bait_name_do_not_search:
            search_response = {'ID': None}
        else:
            search_response = await XivapiWrapper.xivapi_item_search(
                angler_bait_name_corrections.get(bait_angler_name) or bait_angler_name
            )

        return cls(bait_angler_bait_id=bait_angler_id, bait_xivapi_item_id=search_response['ID'])
