#! /usr/bin/env python3

from dataclasses import dataclass, field
from typing import Any, Dict

from dataclasses_json import DataClassJsonMixin

from ff14angler.dataClasses.cache.searchCache import SearchCache
from ff14angler.dataClasses.cache.idIndexCache import IdIndexCache


@dataclass
class XivapiCache(DataClassJsonMixin):
    FishParameter: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    FishingSpot: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    GatheringPoint: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    GatheringPointBase: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    IdIndex: IdIndexCache = field(default_factory=IdIndexCache)
    Item: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    Leve: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    PlaceName: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    SpearfishingItem: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    SpearfishingNotebook: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    SpecialShop: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    Search: SearchCache = field(default_factory=SearchCache)
