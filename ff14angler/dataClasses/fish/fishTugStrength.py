#! /usr/bin/env python3

from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class FishTugStrength:
    fish_tug_strength: int
    fish_tug_strength_percent: float
