#! /usr/bin/env python3

from dataclasses import dataclass, field
from typing import Any, Dict, List, TypedDict, Set

from dataclasses_json import DataClassJsonMixin


GatheringPointBaseSpearfishingIds = TypedDict(
    'GatheringPointBaseSpearfishingIds',
    {
        'game_content_links': List[int],
        'gathering_point_base_id': int,
        'gathering_point_base_level': int,
        'spearfishing_ids': Set[int],
    }
)


@dataclass
class IdIndexCache(DataClassJsonMixin):
    GatheringPointBaseIndex: List[Dict[str, Any]] = field(default_factory=list)
    GatheringPointBaseSpearfishingIndex: List[GatheringPointBaseSpearfishingIds] = field(
        default_factory=list,
        metadata={
            'dataclasses_json': {
                'decoder': lambda index: [
                    {
                        **item,
                        **{'spearfishing_ids': set(item['spearfishing_ids'])}
                    } for item in index
                ]
            }
        }
    )
