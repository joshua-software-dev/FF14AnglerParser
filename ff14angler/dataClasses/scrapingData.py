#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Any, Dict

from ff14angler.dataClasses.bait.bait import Bait
from ff14angler.dataClasses.fish.fish import Fish
from ff14angler.dataClasses.spot.spot import Spot


@dataclass
class ScrapingData:
    bait: Dict[int, Bait]
    fish: Dict[int, Fish]
    spot: Dict[int, Spot]

    @classmethod
    async def get_scraping_data_from_export_json(
        cls,
        input_json: Dict[str, Dict[int, Dict[str, Any]]]
    ) -> 'ScrapingData':
        return cls(
            bait={k: await Bait.get_bait_from_export_json(**v) for k, v in input_json['bait'].items()},
            fish={k: await Fish.get_fish_from_export_json(**v) for k, v in input_json['fish'].items()},
            spot={k: await Spot.get_spot_from_export_json(**v) for k, v in input_json['spot'].items()}
        )
