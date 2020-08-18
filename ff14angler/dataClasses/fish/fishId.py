#! /usr/bin/env python3

from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin

from ff14angler.aiohttpWrapped import AiohttpWrapped


@dataclass
class FishId(DataClassJsonMixin):
    fish_angler_fish_id: int
    fish_xivapi_item_id: int

    @classmethod
    async def get_fish_id_from_angler_fish(cls, fish_angler_id: int, fish_angler_name: str):
        search_response = await AiohttpWrapped.xivapi_item_search(fish_angler_name)
        return cls(fish_angler_fish_id=fish_angler_id, fish_xivapi_item_id=search_response['ID'])
