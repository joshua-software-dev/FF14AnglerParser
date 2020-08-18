#! /usr/bin/env python3

from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class FishTugStrength(DataClassJsonMixin):
    fish_tug_strength: int
    fish_tug_strength_percent: float
