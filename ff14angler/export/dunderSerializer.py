#! /usr/bin/env python3

import dataclasses
import json

from datetime import date, time, datetime, timedelta


class DunderSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (set, frozenset,)):
            return list(obj)
        elif isinstance(obj, (date, time, datetime, timedelta,)):
            return str(obj)
        elif dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        return super().default(obj)
