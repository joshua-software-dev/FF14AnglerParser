#! /usr/bin/env python3

from dataclasses import dataclass, field
from typing import Any, Dict, List

from dataclasses_json import DataClassJsonMixin


@dataclass
class SearchCache(DataClassJsonMixin):
    Item: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    Leve: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    PlaceName: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
