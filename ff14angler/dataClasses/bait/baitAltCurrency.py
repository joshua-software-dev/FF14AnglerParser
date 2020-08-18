#! /usr/bin/env python3

from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class BaitAltCurrency(DataClassJsonMixin):
    bait_alt_currency_id: int
    bait_alt_currency_name: str
    bait_alt_currency_cost: int
