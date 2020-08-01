#! /usr/bin/env python3

from typing import Dict

from ff14angler.dataClasses.fish.fish import Fish


class FishProvider:
    fish_holder: Dict[int, Fish] = dict()

    @classmethod
    def __json__(cls):
        return cls.fish_holder

    @classmethod
    async def get_fish_from_angler_fish(cls, fish_angler_id: int, fish_angler_name: str) -> Fish:
        if result := cls.fish_holder.get(fish_angler_id):
            return result

        cls.fish_holder[fish_angler_id] = await Fish.get_fish_from_angler_fish(fish_angler_id, fish_angler_name)
        return cls.fish_holder[fish_angler_id]
