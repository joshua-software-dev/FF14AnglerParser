#! /usr/bin/env python3

from dataclasses import dataclass, field
from typing import List


@dataclass
class TableExportData:
    header: tuple
    insert_statement: str
    data: List[tuple] = field(default_factory=list)
