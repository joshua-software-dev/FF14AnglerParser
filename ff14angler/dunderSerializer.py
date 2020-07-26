#! /usr/bin/env python3

import json


class DunderSerializer(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj.__json__()
        except AttributeError:
            return json.JSONEncoder.default(self, obj)
