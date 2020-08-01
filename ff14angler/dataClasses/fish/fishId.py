#! /usr/bin/env python3

from dataclasses import dataclass

from ...aiohttpWrapped import AiohttpWrapped


@dataclass
class FishId:
    angler_fish_id: int
    xivapi_item_id: int

    def __json__(self):
        return self.__dict__

    @classmethod
    async def get_fish_id_from_angler_fish(cls, fish_angler_id: int, fish_angler_name: str):
        search_response = await AiohttpWrapped.xivapi_item_search(fish_angler_name)
        return cls(angler_fish_id=fish_angler_id, xivapi_item_id=search_response['ID'])
