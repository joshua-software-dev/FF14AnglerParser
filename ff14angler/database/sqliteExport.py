#! /usr/bin/env python3

import asyncio
import os
import sqlite3

from ff14angler.constants.values import ANGLER_API_BASE_URL, SQLITE_DIRECTORY, SQLITE_DATABASE
from ff14angler.dataClasses.scrapingData import ScrapingData


class SQLiteExport:

    @staticmethod
    async def create_database_from_schema() -> sqlite3.Connection:
        try:
            os.remove(SQLITE_DATABASE)
        except FileNotFoundError:
            pass

        conn = sqlite3.connect(SQLITE_DATABASE)
        cursor = conn.cursor()

        for file in sorted(filter(lambda x: x.endswith('.sql'), os.listdir(SQLITE_DIRECTORY))):
            with open(os.path.join(SQLITE_DIRECTORY, file)) as fh:
                statements = fh.read().strip()

            for statement in statements.split('\n\n'):
                success = False
                while not success:
                    for attempt in range(3):
                        try:
                            cursor.execute(statement)
                            success = True
                            break
                        except sqlite3.OperationalError:  # Database is locked
                            if attempt < 2:
                                await asyncio.sleep(1)
                            else:
                                raise

        conn.commit()
        cursor.close()
        return conn

    @staticmethod
    async def export_bait_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for bait in scraping_data.bait.values():
            cursor.execute(
                'INSERT INTO `bait` VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                (
                    bait.bait_id.bait_angler_bait_id,
                    bait.bait_id.bait_xivapi_item_id,
                    bait.bait_angler_name,
                    bait.bait_item_name,
                    bait.bait_icon_url,
                    bait.bait_large_icon_url,
                    bait.bait_angler_lodestone_url,
                    bait.bait_item_level,
                    bait.bait_gil_cost,
                    bait.bait_gil_sell_price,
                    bait.bait_angler_is_mooch_fish,
                )
            )

    @staticmethod
    async def export_fish_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for fish in scraping_data.fish.values():
            cursor.execute(
                'INSERT INTO `fish` VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                (
                    fish.fish_id.fish_angler_fish_id,
                    fish.fish_id.fish_xivapi_item_id,
                    fish.fish_angler_name,
                    fish.fish_item_name,
                    fish.fish_icon_url,
                    fish.fish_large_icon_url,
                    fish.fish_angler_lodestone_url,
                    fish.fish_item_level,
                    fish.fish_short_description,
                    fish.fish_long_description,
                    fish.fish_introduced_patch,
                    fish.fish_angler_territory,
                    fish.fish_angler_item_category,
                    fish.fish_angler_double_hooking_count,
                    fish.fish_angler_aquarium_size,
                    fish.fish_angler_canvas_size,
                )
            )

    @staticmethod
    async def export_spot_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for spot in scraping_data.spot.values():
            cursor.execute(
                'INSERT INTO `spot` VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                (
                    spot.spot_id.spot_angler_spot_id,
                    spot.spot_id.spot_gathering_type.gathering_type,
                    spot.spot_id.spot_gathering_type.gathering_type_unique_id,
                    spot.spot_angler_area_id,
                    spot.spot_angler_name,
                    spot.spot_angler_zone_name,
                    spot.spot_gathering_level,
                    spot.spot_angler_x_coord,
                    spot.spot_angler_y_coord,
                    spot.spot_angler_fishers_intuition_comment,
                )
            )

    @staticmethod
    async def export_comment_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        comment_set = set()

        for bait in scraping_data.bait.values():
            if bait.bait_angler_comments:
                for comment in bait.bait_angler_comments.comments:
                    if comment not in comment_set:
                        comment_set.add(comment)
                        cursor.execute(
                            'INSERT INTO `comment` VALUES (?, ?, ?, ?, ?, ?);',
                            (
                                comment.unique_id.bytes,
                                bait.bait_angler_comments.comment_fetch_timestamp,
                                comment.comment_timestamp,
                                comment.comment_author,
                                comment.comment_text_original,
                                comment.comment_text_translated,
                            )
                        )

        for fish in scraping_data.fish.values():
            if fish.fish_angler_comments:
                for comment in fish.fish_angler_comments.comments:
                    if comment not in comment_set:
                        comment_set.add(comment)
                        cursor.execute(
                            'INSERT INTO `comment` VALUES (?, ?, ?, ?, ?, ?);',
                            (
                                comment.unique_id.bytes,
                                fish.fish_angler_comments.comment_fetch_timestamp,
                                comment.comment_timestamp,
                                comment.comment_author,
                                comment.comment_text_original,
                                comment.comment_text_translated,
                            )
                        )

        for spot in scraping_data.spot.values():
            if spot.spot_angler_comments:
                for comment in spot.spot_angler_comments.comments:
                    if comment not in comment_set:
                        comment_set.add(comment)
                        cursor.execute(
                            'INSERT INTO `comment` VALUES (?, ?, ?, ?, ?, ?);',
                            (
                                comment.unique_id.bytes,
                                spot.spot_angler_comments.comment_fetch_timestamp,
                                comment.comment_timestamp,
                                comment.comment_author,
                                comment.comment_text_original,
                                comment.comment_text_translated,
                            )
                        )

    @staticmethod
    async def export_bait_comment_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for bait in scraping_data.bait.values():
            if bait.bait_angler_comments:
                for comment in bait.bait_angler_comments.comments:
                    cursor.execute(
                        'INSERT INTO `bait_comment` VALUES (?, ?);',
                        (
                            bait.bait_id.bait_angler_bait_id,
                            comment.unique_id.bytes,
                        )
                    )

    @staticmethod
    async def export_fish_comment_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for fish in scraping_data.fish.values():
            if fish.fish_angler_comments:
                for comment in fish.fish_angler_comments.comments:
                    cursor.execute(
                        'INSERT INTO `fish_comment` VALUES (?, ?);',
                        (
                            fish.fish_id.fish_angler_fish_id,
                            comment.unique_id.bytes,
                        )
                    )

    @staticmethod
    async def export_spot_comment_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for spot in scraping_data.spot.values():
            if spot.spot_angler_comments:
                for comment in spot.spot_angler_comments.comments:
                    cursor.execute(
                        'INSERT INTO `spot_comment` VALUES (?, ?);',
                        (
                            spot.spot_id.spot_angler_spot_id,
                            str(comment.unique_id),
                        )
                    )

    @staticmethod
    async def export_bait_alt_currency_price_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for bait in scraping_data.bait.values():
            for alt_currency in bait.bait_alt_currency_prices:
                cursor.execute(
                    'INSERT INTO `bait_alt_currency_price` VALUES (?, ?, ?, ?);',
                    (
                        bait.bait_id.bait_angler_bait_id,
                        alt_currency.bait_alt_currency_id,
                        alt_currency.bait_alt_currency_cost,
                        alt_currency.bait_alt_currency_name,
                    )
                )

    @staticmethod
    async def export_fish_bait_preference_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for fish in scraping_data.fish.values():
            for bait_pref in fish.fish_angler_bait_preferences:
                cursor.execute(
                    'INSERT INTO `fish_bait_preference` VALUES (?, ?, ?);',
                    (
                        fish.fish_id.fish_angler_fish_id,
                        bait_pref.bait_id.bait_angler_bait_id,
                        bait_pref.bait_percentage,
                    )
                )

    @staticmethod
    async def export_fish_caught_count(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for fish in scraping_data.fish.values():
            hour_preferences = fish.fish_angler_hour_preferences
            if hour_preferences:
                hour_catch_count = hour_preferences.unique_catches_across_all_hours
            else:
                hour_catch_count = None

            weather_preferences = fish.fish_angler_weather_preferences
            if weather_preferences:
                weather_catch_count = weather_preferences.unique_catches_across_all_weathers
            else:
                weather_catch_count = None

            cursor.execute(
                'INSERT INTO `fish_caught_count` VALUES (?, ?, ?);',
                (
                    fish.fish_id.fish_angler_fish_id,
                    hour_catch_count,
                    weather_catch_count,
                )
            )

    @staticmethod
    async def export_fish_caught_per_hour_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for fish in scraping_data.fish.values():
            if fish.fish_angler_hour_preferences:
                for hour_num, count in fish.fish_angler_hour_preferences.hours.items():
                    cursor.execute(
                        'INSERT INTO `fish_caught_per_hour` VALUES (?, ?, ?);',
                        (
                            fish.fish_id.fish_angler_fish_id,
                            hour_num,
                            count,
                        )
                    )

    @staticmethod
    async def export_fish_caught_per_weather_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for fish in scraping_data.fish.values():
            weather_preferences = fish.fish_angler_weather_preferences
            if weather_preferences:
                for weather_name, count in weather_preferences.weathers.items():
                    cursor.execute(
                        'INSERT INTO `fish_caught_per_weather` VALUES (?, ?, ?);',
                        (
                            fish.fish_id.fish_angler_fish_id,
                            weather_name,
                            count,
                        )
                    )

    @staticmethod
    async def export_fish_desynthesis_item_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for fish in scraping_data.fish.values():
            for item in fish.fish_angler_desynthesis_items:
                cursor.execute(
                    'INSERT INTO `fish_desynthesis_item` VALUES (?, ?, ?, ?, ?, ?, ?, ?);',
                    (
                        fish.fish_id.fish_angler_fish_id,
                        item.desynthesis_item_id,
                        item.desynthesis_item_name,
                        item.desynthesis_icon_url,
                        item.desynthesis_large_icon_url,
                        item.desynthesis_angler_item_name,
                        item.desynthesis_angler_lodestone_url,
                        item.desynthesis_angler_percentage,
                    )
                )

    @staticmethod
    async def export_fish_involved_leve_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for fish in scraping_data.fish.values():
            for leve in fish.fish_angler_involved_leves:
                cursor.execute(
                    'INSERT INTO `fish_involved_leve` VALUES (?, ?, ?, ?, ?, ?, ?);',
                    (
                        fish.fish_id.fish_angler_fish_id,
                        leve.leve_id,
                        leve.leve_name,
                        leve.leve_angler_name,
                        leve.leve_angler_name_jp,
                        leve.leve_level,
                        leve.leve_angler_turn_in_count,
                    )
                )

    @staticmethod
    async def export_fish_involved_recipe_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for fish in scraping_data.fish.values():
            for recipe in fish.fish_angler_involved_recipes:
                cursor.execute(
                    'INSERT INTO `fish_involved_recipe` VALUES (?, ?, ?, ?, ?, ?, ?, ?);',
                    (
                        fish.fish_id.fish_angler_fish_id,
                        recipe.recipe_item_id,
                        recipe.recipe_name,
                        recipe.recipe_angler_name,
                        recipe.recipe_icon_url,
                        recipe.recipe_large_icon_url,
                        recipe.recipe_angler_lodestone_url,
                        recipe.recipe_angler_crafting_class,
                    )
                )

    @staticmethod
    async def export_fish_tug_strength_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for fish in scraping_data.fish.values():
            for tug_strength in fish.fish_angler_tug_strength:
                cursor.execute(
                    'INSERT INTO `fish_tug_strength` VALUES (?, ?, ?);',
                    (
                        fish.fish_id.fish_angler_fish_id,
                        tug_strength.fish_tug_strength,
                        tug_strength.fish_tug_strength_percent,
                    )
                )

    @staticmethod
    async def export_spot_available_fish_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for spot in scraping_data.spot.values():
            for fish_id in spot.spot_angler_catch_metadata.spot_available_fish:
                cursor.execute(
                    'INSERT INTO `spot_available_fish` (spot_angler_spot_id, fish_angler_fish_id) VALUES (?, ?);',
                    (
                        spot.spot_id.spot_angler_spot_id,
                        fish_id.fish_angler_fish_id,
                    )
                )

    @staticmethod
    async def export_spot_bait_fish_catch_info_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for spot in scraping_data.spot.values():
            for metadata in spot.spot_angler_catch_metadata.spot_fish_caught_per_bait:
                for fish in metadata.spot_angler_bait_fish_catch_info:
                    cursor.execute(
                        'INSERT INTO `spot_bait_fish_catch_info` VALUES (?, ?, ?, ?, ?, ?);',
                        (
                            spot.spot_id.spot_angler_spot_id,
                            metadata.spot_bait_id.bait_angler_bait_id,
                            fish.spot_fish_id.fish_angler_fish_id,
                            fish.spot_angler_fish_caught_count,
                            fish.spot_angler_fish_average_seconds_to_hook,
                            fish.spot_angler_fish_caught_percentage,
                        )
                    )

    @staticmethod
    async def export_spot_bait_total_fish_caught_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for spot in scraping_data.spot.values():
            for metadata in spot.spot_angler_catch_metadata.spot_fish_caught_per_bait:
                if metadata.spot_angler_bait_total_fish_caught is not None:
                    cursor.execute(
                        'INSERT INTO `spot_bait_total_fish_caught` VALUES (?, ?, ?);',
                        (
                            spot.spot_id.spot_angler_spot_id,
                            metadata.spot_bait_id.bait_angler_bait_id,
                            metadata.spot_angler_bait_total_fish_caught,
                        )
                    )

    @staticmethod
    async def export_spot_effective_bait_table(cursor: sqlite3.Cursor, scraping_data: ScrapingData):
        for spot in scraping_data.spot.values():
            for bait_id in spot.spot_angler_catch_metadata.spot_effective_bait:
                cursor.execute(
                    'INSERT INTO `spot_effective_bait` (spot_angler_spot_id, bait_angler_bait_id) VALUES (?, ?);',
                    (
                        spot.spot_id.spot_angler_spot_id,
                        bait_id.bait_angler_bait_id,
                    )
                )

    @classmethod
    async def output_data_as_database(cls, scraping_data: ScrapingData):
        conn = await cls.create_database_from_schema()
        cursor = conn.cursor()

        try:
            await cls.export_bait_table(cursor, scraping_data)
            await cls.export_fish_table(cursor, scraping_data)
            await cls.export_spot_table(cursor, scraping_data)
            await cls.export_comment_table(cursor, scraping_data)
            await cls.export_bait_comment_table(cursor, scraping_data)
            await cls.export_fish_comment_table(cursor, scraping_data)
            await cls.export_spot_comment_table(cursor, scraping_data)
            await cls.export_bait_alt_currency_price_table(cursor, scraping_data)
            await cls.export_fish_bait_preference_table(cursor, scraping_data)
            await cls.export_fish_caught_count(cursor, scraping_data)
            await cls.export_fish_caught_per_hour_table(cursor, scraping_data)
            await cls.export_fish_caught_per_weather_table(cursor, scraping_data)
            await cls.export_fish_desynthesis_item_table(cursor, scraping_data)
            await cls.export_fish_involved_leve_table(cursor, scraping_data)
            await cls.export_fish_involved_recipe_table(cursor, scraping_data)
            await cls.export_fish_tug_strength_table(cursor, scraping_data)
            await cls.export_spot_available_fish_table(cursor, scraping_data)
            await cls.export_spot_bait_fish_catch_info_table(cursor, scraping_data)
            await cls.export_spot_bait_total_fish_caught_table(cursor, scraping_data)
            await cls.export_spot_effective_bait_table(cursor, scraping_data)
            conn.commit()
        finally:
            cursor.close()
            conn.close()
