#! /usr/bin/env python3

import re


angler_map_area_matcher_regex = re.compile(r"area=([0-9]+)&")
angler_map_x_coord_matcher_regex = re.compile(r"x=([0-9]+)&")
angler_map_y_coord_matcher_regex = re.compile(r"y=([0-9]+)")
angler_bait_metadata_catch_count_regex = re.compile(r"\((\d+)/(\d+)\)$")
desynthesis_quantity_matcher_regex = re.compile(r"\((\s+)?\d+(\s+)?~(\s+)?\d+(\s+)?\)$")
non_number_replacement_regex = re.compile(r"[^\d]")
timestamp_matcher_regex = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
