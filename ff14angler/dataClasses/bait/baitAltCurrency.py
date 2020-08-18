#! /usr/bin/env python3

from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BaitAltCurrency:
    bait_alt_currency_id: int
    bait_alt_currency_name: str
    bait_alt_currency_cost: int
