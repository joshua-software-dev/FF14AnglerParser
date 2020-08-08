#! /usr/bin/env python3

from dataclasses import dataclass


@dataclass
class BaitAltCurrency:
    bait_alt_currency_id: int
    bait_alt_currency_name: str
    bait_alt_currency_cost: int
