#! /usr/bin/env python3

from dataclasses import dataclass


@dataclass
class FishTugStrength:
    fish_tug_strength: int
    fish_tug_strength_percent: float

    def __json__(self):
        return self.__dict__
