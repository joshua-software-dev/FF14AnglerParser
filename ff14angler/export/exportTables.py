#! /usr/bin/env python3

import csv
import os

from typing import Any, Dict


PostJsonHomePageData = Dict[str, Dict[int, Dict[str, Any]]]


class ExportTables:

    @staticmethod
    async def export_bait_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/001_bait.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'bait_angler_bait_id',
                    'bait_xivapi_item_id',
                    'bait_angler_name',
                    'bait_item_name',
                    'bait_icon_url',
                    'bait_large_icon_url',
                    'bait_lodestone_url',
                    'bait_item_level',
                    'bait_gil_cost',
                    'bait_gil_sell_price',
                    'bait_is_mooch_fish'
                ]
            )

            for bait in home_page_data['bait'].values():
                writer.writerow(
                    [
                        bait['bait_id']['bait_angler_bait_id'],
                        bait['bait_id']['bait_xivapi_item_id'],
                        bait['bait_angler_name'],
                        bait['bait_item_name'],
                        bait['bait_icon_url'],
                        bait['bait_angler_large_icon_url'],
                        bait['bait_angler_lodestone_url'],
                        bait['bait_item_level'],
                        bait['bait_gil_cost'],
                        bait['bait_gil_sell_price'],
                        bait['bait_angler_is_mooch_fish']
                    ]
                )

    @staticmethod
    async def export_fish_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/002_fish.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'fish_angler_fish_id',
                    'fish_xivapi_item_id',
                    'fish_angler_name',
                    'fish_item_name',
                    'fish_icon_url',
                    'fish_angler_large_icon_url',
                    'fish_angler_lodestone_url',
                    'fish_item_level',
                    'fish_short_description',
                    'fish_long_description',
                    'fish_introduced_patch',
                    'fish_angler_territory',
                    'fish_angler_item_category',
                    'fish_angler_double_hooking_count',
                    'fish_angler_aquarium_size',
                    'fish_angler_canvas_size'
                ]
            )

            for fish in home_page_data['fish'].values():
                writer.writerow(
                    [
                        fish['fish_id']['fish_angler_fish_id'],
                        fish['fish_id']['fish_xivapi_item_id'],
                        fish['fish_angler_name'],
                        fish['fish_item_name'],
                        fish['fish_icon_url'],
                        fish['fish_angler_large_icon_url'],
                        fish['fish_angler_lodestone_url'],
                        fish['fish_item_level'],
                        fish['fish_short_description'],
                        fish['fish_long_description'],
                        fish['fish_introduced_patch'],
                        fish['fish_angler_territory'],
                        fish['fish_angler_item_category'],
                        fish['fish_angler_double_hooking_count'],
                        fish['fish_angler_aquarium_size'],
                        fish['fish_angler_canvas_size']
                    ]
                )

    @staticmethod
    async def export_spot_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/003_spot.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'spot_angler_spot_id',
                    'spot_gathering_type',
                    'spot_gathering_type_unique_id',
                    'spot_angler_area_id',
                    'spot_angler_name',
                    'spot_angler_zone_name',
                    'spot_gathering_level',
                    'spot_angler_x_coord',
                    'spot_angler_y_coord',
                    'spot_angler_fishers_intuition_comment'
                ]
            )

            for spot in home_page_data['spot'].values():
                writer.writerow(
                    [
                        spot['spot_id']['spot_angler_spot_id'],
                        spot['spot_id']['spot_gathering_type']['gathering_type'],
                        spot['spot_id']['spot_gathering_type']['gathering_type_unique_id'],
                        spot['spot_angler_area_id'],
                        spot['spot_angler_name'],
                        spot['spot_angler_zone_name'],
                        spot['spot_gathering_level'],
                        spot['spot_angler_x_coord'],
                        spot['spot_angler_y_coord'],
                        spot['spot_angler_fishers_intuition_comment']
                    ]
                )

    @staticmethod
    async def export_bait_comment_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/004_bait_comment.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'bait_angler_bait_id',
                    'comment_fetch_timestamp',
                    'comment_timestamp',
                    'comment_author',
                    'comment_text_original',
                    'comment_text_translated'
                ]
            )

            for bait in home_page_data['bait'].values():
                if bait['bait_angler_comments']:
                    for comment in bait['bait_angler_comments']['comments']:
                        writer.writerow(
                            [
                                bait['bait_id']['bait_angler_bait_id'],
                                bait['bait_angler_comments']['comment_fetch_timestamp'],
                                comment['comment_timestamp'],
                                comment['comment_author'],
                                comment['comment_text_original'],
                                comment['comment_text_translated']
                            ]
                        )

    @staticmethod
    async def export_fish_comment_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/005_fish_comment.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'fish_angler_fish_id',
                    'comment_fetch_timestamp',
                    'comment_timestamp',
                    'comment_author',
                    'comment_text_original',
                    'comment_text_translated'
                ]
            )

            for fish in home_page_data['fish'].values():
                for comment in fish['fish_angler_comments']['comments']:
                    writer.writerow(
                        [
                            fish['fish_id']['fish_angler_fish_id'],
                            fish['fish_angler_comments']['comment_fetch_timestamp'],
                            comment['comment_timestamp'],
                            comment['comment_author'],
                            comment['comment_text_original'],
                            comment['comment_text_translated']
                        ]
                    )

    @staticmethod
    async def export_spot_comment_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/006_spot_comment.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'spot_angler_spot_id',
                    'comment_fetch_timestamp',
                    'comment_timestamp',
                    'comment_author',
                    'comment_text_original',
                    'comment_text_translated'
                ]
            )

            for spot in home_page_data['spot'].values():
                for comment in spot['spot_angler_comments']['comments']:
                    writer.writerow(
                        [
                            spot['spot_id']['spot_angler_spot_id'],
                            spot['spot_angler_comments']['comment_fetch_timestamp'],
                            comment['comment_timestamp'],
                            comment['comment_author'],
                            comment['comment_text_original'],
                            comment['comment_text_translated']
                        ]
                    )

    @staticmethod
    async def export_bait_alt_currency_price_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/007_bait_alt_currency_price.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'bait_angler_bait_id',
                    'bait_alt_currency_id',
                    'bait_alt_currency_cost',
                    'bait_alt_currency_name'
                ]
            )

            for bait in home_page_data['bait'].values():
                for alt_currency in bait['bait_alt_currency_prices']:
                    writer.writerow(
                        [
                            bait['bait_id']['bait_angler_bait_id'],
                            alt_currency['bait_alt_currency_id'],
                            alt_currency['bait_alt_currency_cost'],
                            alt_currency['bait_alt_currency_name']
                        ]
                    )

    @staticmethod
    async def export_fish_bait_preference_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/008_fish_bait_preference.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'fish_angler_fish_id',
                    'bait_angler_bait_id',
                    'bait_percentage'
                ]
            )

            for fish in home_page_data['fish'].values():
                for bait_pref in fish['fish_angler_bait_preferences']:
                    writer.writerow(
                        [
                            fish['fish_id']['fish_angler_fish_id'],
                            bait_pref['bait_id']['bait_angler_bait_id'],
                            bait_pref['bait_percentage']
                        ]
                    )

    @staticmethod
    async def export_fish_caught_count(home_page_data: PostJsonHomePageData):
        with open('data/table_data/009_fish_caught_count.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'fish_angler_fish_id',
                    'fish_caught_all_hours_count',
                    'fish_caught_all_weathers_count'
                ]
            )

            for fish in home_page_data['fish'].values():
                weather_preferences = fish['fish_angler_weather_preferences']
                if weather_preferences:
                    weather_catch_count = weather_preferences['unique_catches_across_all_weathers']
                else:
                    weather_catch_count = None

                writer.writerow(
                    [
                        fish['fish_id']['fish_angler_fish_id'],
                        fish['fish_angler_hour_preferences']['unique_catches_across_all_hours'],
                        weather_catch_count
                    ]
                )

    @staticmethod
    async def export_fish_caught_per_hour_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/010_fish_caught_per_hour.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'fish_angler_fish_id',
                    'hour_num',
                    'hour_fish_caught_count'
                ]
            )

            for fish in home_page_data['fish'].values():
                for hour_num, count in fish['fish_angler_hour_preferences']['hours'].items():
                    writer.writerow(
                        [
                            fish['fish_id']['fish_angler_fish_id'],
                            hour_num,
                            count
                        ]
                    )

    @staticmethod
    async def export_fish_caught_per_weather_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/011_fish_caught_per_weather.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'fish_angler_fish_id',
                    'weather_name',
                    'weather_fish_caught_count'
                ]
            )

            for fish in home_page_data['fish'].values():
                weather_preferences = fish['fish_angler_weather_preferences']
                if weather_preferences:
                    for weather_name, count in weather_preferences['weathers'].items():
                        writer.writerow(
                            [
                                fish['fish_id']['fish_angler_fish_id'],
                                weather_name,
                                count
                            ]
                        )

    @staticmethod
    async def export_fish_desynthesis_item_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/012_fish_desynthesis_item.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'fish_angler_fish_id',
                    'desynthesis_item_id',
                    'desynthesis_item_name',
                    'desynthesis_icon_url',
                    'desynthesis_angler_item_name',
                    'desynthesis_angler_lodestone_url',
                    'desynthesis_angler_percentage'
                ]
            )

            for fish in home_page_data['fish'].values():
                for item in fish['fish_angler_desynthesis_items']:
                    writer.writerow(
                        [
                            fish['fish_id']['fish_angler_fish_id'],
                            item['desynthesis_item_id'],
                            item['desynthesis_item_name'],
                            item['desynthesis_icon_url'],
                            item['desynthesis_angler_item_name'],
                            item['desynthesis_angler_lodestone_url'],
                            item['desynthesis_angler_percentage']
                        ]
                    )

    @staticmethod
    async def export_fish_involved_leve_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/013_fish_involved_leve.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'fish_angler_fish_id',
                    'leve_id',
                    'leve_name',
                    'leve_angler_name',
                    'leve_angler_name_jp',
                    'leve_level',
                    'leve_angler_turn_in_count'
                ]
            )

            for fish in home_page_data['fish'].values():
                for leve in fish['fish_angler_involved_leves']:
                    writer.writerow(
                        [
                            fish['fish_id']['fish_angler_fish_id'],
                            leve['leve_id'],
                            leve['leve_name'],
                            leve['leve_angler_name'],
                            leve['leve_angler_name_jp'],
                            leve['leve_level'],
                            leve['leve_angler_turn_in_count']
                        ]
                    )

    @staticmethod
    async def export_fish_involved_recipe_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/014_fish_involved_recipe.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'fish_angler_fish_id',
                    'recipe_item_id',
                    'recipe_item_name',
                    'recipe_angler_name',
                    'recipe_icon_url',
                    'recipe_angler_lodestone_url',
                    'recipe_angler_crafting_class'
                ]
            )

            for fish in home_page_data['fish'].values():
                for recipe in fish['fish_angler_involved_recipes']:
                    writer.writerow(
                        [
                            fish['fish_id']['fish_angler_fish_id'],
                            recipe['recipe_item_id'],
                            recipe['recipe_name'],
                            recipe['recipe_angler_name'],
                            recipe['recipe_icon'],
                            recipe['recipe_angler_lodestone_url'],
                            recipe['recipe_angler_crafting_class']
                        ]
                    )

    @staticmethod
    async def export_fish_tug_strength_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/015_fish_tug_strength.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'fish_angler_fish_id',
                    'tug_strength',
                    'tug_strength_percent'
                ]
            )

            for fish in home_page_data['fish'].values():
                for tug_strength in fish['fish_angler_tug_strength']:
                    writer.writerow(
                        [
                            fish['fish_id']['fish_angler_fish_id'],
                            tug_strength['fish_tug_strength'],
                            tug_strength['fish_tug_strength_percent']
                        ]
                    )

    @staticmethod
    async def export_spot_available_fish_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/016_spot_available_fish.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'spot_angler_spot_id',
                    'fish_angler_fish_id'
                ]
            )

            for spot in home_page_data['spot'].values():
                for fish_id in spot['spot_angler_catch_metadata']['spot_available_fish']:
                    writer.writerow(
                        [
                            spot['spot_id']['spot_angler_spot_id'],
                            fish_id['fish_angler_fish_id']
                        ]
                    )

    @staticmethod
    async def export_spot_bait_fish_catch_info_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/017_spot_bait_fish_catch_info.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'spot_angler_spot_id',
                    'bait_angler_bait_id',
                    'fish_angler_fish_id',
                    'spot_bait_fish_catch_count',
                    'spot_bait_fish_average_seconds_to_hook',
                    'spot_bait_fish_catch_percentage'
                ]
            )

            for spot in home_page_data['spot'].values():
                for metadata in spot['spot_angler_catch_metadata']['spot_fish_caught_per_bait']:
                    for fish in metadata['spot_angler_bait_fish_catch_info']:
                        writer.writerow(
                            [
                                spot['spot_id']['spot_angler_spot_id'],
                                metadata['spot_bait_id']['bait_angler_bait_id'],
                                fish['spot_fish_id']['fish_angler_fish_id'],
                                fish['spot_angler_fish_caught_count'],
                                fish['spot_angler_fish_average_seconds_to_hook'],
                                fish['spot_angler_fish_caught_percentage']
                            ]
                        )

    @staticmethod
    async def export_spot_bait_total_fish_caught_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/018_spot_bait_total_fish_caught.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'spot_angler_spot_id',
                    'bait_angler_bait_id',
                    'spot_bait_total_catch_count'
                ]
            )

            for spot in home_page_data['spot'].values():
                for metadata in spot['spot_angler_catch_metadata']['spot_fish_caught_per_bait']:
                    writer.writerow(
                        [
                            spot['spot_id']['spot_angler_spot_id'],
                            metadata['spot_bait_id']['bait_angler_bait_id'],
                            metadata['spot_angler_bait_total_fish_caught']
                        ]
                    )

    @staticmethod
    async def export_spot_effective_bait_table(home_page_data: PostJsonHomePageData):
        with open('data/table_data/019_spot_effective_bait.csv', 'w+') as fh:
            writer = csv.writer(fh, delimiter=',', lineterminator='\n')
            writer.writerow(
                [
                    'spot_angler_spot_id',
                    'bait_angler_bait_id'
                ]
            )

            for spot in home_page_data['spot'].values():
                for bait_id in spot['spot_angler_catch_metadata']['spot_effective_bait']:
                    writer.writerow(
                        [
                            spot['spot_id']['spot_angler_spot_id'],
                            bait_id['bait_angler_bait_id']
                        ]
                    )

    @classmethod
    async def output_data_for_database(cls, home_page_data: PostJsonHomePageData):
        os.makedirs('data/table_data/', exist_ok=True)
        await cls.export_bait_table(home_page_data)
        await cls.export_fish_table(home_page_data)
        await cls.export_spot_table(home_page_data)
        await cls.export_bait_comment_table(home_page_data)
        await cls.export_fish_comment_table(home_page_data)
        await cls.export_spot_comment_table(home_page_data)
        await cls.export_bait_alt_currency_price_table(home_page_data)
        await cls.export_fish_bait_preference_table(home_page_data)
        await cls.export_fish_caught_count(home_page_data)
        await cls.export_fish_caught_per_hour_table(home_page_data)
        await cls.export_fish_caught_per_weather_table(home_page_data)
        await cls.export_fish_desynthesis_item_table(home_page_data)
        await cls.export_fish_involved_leve_table(home_page_data)
        await cls.export_fish_involved_recipe_table(home_page_data)
        await cls.export_fish_tug_strength_table(home_page_data)
        await cls.export_spot_available_fish_table(home_page_data)
        await cls.export_spot_bait_fish_catch_info_table(home_page_data)
        await cls.export_spot_bait_total_fish_caught_table(home_page_data)
        await cls.export_spot_effective_bait_table(home_page_data)
