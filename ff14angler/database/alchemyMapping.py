#! /usr/bin/env python3

import uuid

from sqlalchemy import (
    BigInteger,
    Binary,
    Column,
    DECIMAL,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    types
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# noinspection PyAbstractClass
class UUID(types.TypeDecorator):
    impl = Binary

    def __init__(self):
        self.impl.length = 16
        types.TypeDecorator.__init__(self, length=self.impl.length)

    def process_bind_param(self, value, dialect=None):
        if value and isinstance(value, uuid.UUID):
            return value.bytes
        elif value and not isinstance(value, uuid.UUID):
            raise ValueError(f'value {value} is not a valid uuid.UUID')
        else:
            return None

    def process_result_value(self, value, dialect=None):
        if value:
            return str(uuid.UUID(bytes=value))
        else:
            return None

    @staticmethod
    def is_mutable():
        return False


# noinspection SpellCheckingInspection
class Bait(Base):
    __tablename__ = 'bait'

    bait_angler_bait_id = Column(BigInteger, primary_key=True)
    bait_xivapi_item_id = Column(BigInteger, nullable=False, index=True)
    bait_angler_name = Column(String(4096), nullable=False)
    bait_item_name = Column(String(4096), nullable=False)
    bait_icon_url = Column(String(2083), nullable=False)
    bait_large_icon_url = Column(String(2083))
    bait_lodestone_url = Column(String(2083))
    bait_item_level = Column(SmallInteger, nullable=False)
    bait_gil_cost = Column(Integer)
    bait_gil_sell_price = Column(Integer)
    bait_is_mooch_fish = Column(Integer, nullable=False)

    comment = relationship('Comment', secondary='bait_comment')
    spot_angler_spots = relationship('Spot', secondary='spot_effective_bait')


# noinspection SpellCheckingInspection
class Fish(Base):
    __tablename__ = 'fish'

    fish_angler_fish_id = Column(BigInteger, primary_key=True)
    fish_xivapi_item_id = Column(BigInteger, nullable=False, index=True)
    fish_angler_name = Column(String(4096), nullable=False)
    fish_item_name = Column(String(4096), nullable=False)
    fish_icon_url = Column(String(2083), nullable=False)
    fish_large_icon_url = Column(String(2083))
    fish_lodestone_url = Column(String(2083))
    fish_item_level = Column(SmallInteger, nullable=False)
    fish_short_description = Column(Text, nullable=False)
    fish_long_description = Column(Text)
    fish_introduced_patch = Column(String(8), nullable=False)
    fish_angler_territory = Column(String(128))
    fish_angler_item_category = Column(String(128), nullable=False)
    fish_angler_double_hooking_count = Column(String(8), nullable=False)
    fish_angler_aquarium_size = Column(String(8))
    fish_angler_canvas_size = Column(String(8))

    spot_angler_spots = relationship('Spot', secondary='spot_available_fish')


# noinspection SpellCheckingInspection
class Spot(Base):
    __tablename__ = 'spot'
    __table_args__ = (
        Index('spot_spot_gathering_type', 'spot_gathering_type', 'spot_gathering_type_unique_id'),
    )

    spot_angler_spot_id = Column(BigInteger, primary_key=True)
    spot_gathering_type = Column(Text, nullable=False)
    spot_gathering_type_unique_id = Column(BigInteger, nullable=False)
    spot_angler_area_id = Column(BigInteger, nullable=False)
    spot_angler_name = Column(String(4096), nullable=False)
    spot_angler_zone_name = Column(String(4096), nullable=False)
    spot_gathering_level = Column(SmallInteger, nullable=False)
    spot_angler_x_coord = Column(SmallInteger, nullable=False)
    spot_angler_y_coord = Column(SmallInteger, nullable=False)
    spot_angler_fishers_intuition_comment = Column(String(512))


# noinspection SpellCheckingInspection,SpellCheckingInspection
class Comment(Base):
    __tablename__ = 'comment'

    comment_uuid = Column(UUID(), primary_key=True)
    comment_fetch_timestamp = Column(DateTime, nullable=False)
    comment_timestamp = Column(DateTime, nullable=False)
    comment_author = Column(String(256), nullable=False)
    comment_text_original = Column(String(160), nullable=False)
    comment_text_translated = Column(String(160), nullable=False)

    fish_angler_fishs = relationship('Fish', secondary='fish_comment')
    spot_angler_spots = relationship('Spot', secondary='spot_comment')


# noinspection SpellCheckingInspection
class BaitComment(Comment):
    __tablename__ = 'bait_comment'

    bait_angler_bait_id = Column(ForeignKey('bait.bait_angler_bait_id'), primary_key=True, nullable=False, index=True)
    comment_uuid = Column(ForeignKey('comment.comment_uuid'), primary_key=True, nullable=False)


# noinspection SpellCheckingInspection
class FishComment(Comment):
    __tablename__ = 'fish_comment'

    fish_angler_fish_id = Column(ForeignKey('fish.fish_angler_fish_id'), primary_key=True, nullable=False, index=True)
    comment_uuid = Column(ForeignKey('comment.comment_uuid'), primary_key=True, nullable=False)


# noinspection SpellCheckingInspection
class SpotComment(Comment):
    __tablename__ = 'spot_comment'

    spot_angler_spot_id = Column(ForeignKey('spot.spot_angler_spot_id'), primary_key=True, nullable=False, index=True)
    comment_uuid = Column(ForeignKey('comment.comment_uuid'), primary_key=True, nullable=False)


# noinspection SpellCheckingInspection
class BaitAltCurrencyPrice(Base):
    __tablename__ = 'bait_alt_currency_price'

    bait_angler_bait_id = Column(ForeignKey('bait.bait_angler_bait_id'), primary_key=True, nullable=False, index=True)
    bait_alt_currency_id = Column(BigInteger, primary_key=True, nullable=False)
    bait_alt_currency_cost = Column(Integer, primary_key=True, nullable=False)
    bait_alt_currency_name = Column(String(4096), nullable=False)

    bait_angler_bait = relationship('Bait')


# noinspection SpellCheckingInspection
class FishBaitPreference(Base):
    __tablename__ = 'fish_bait_preference'

    fish_angler_fish_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    bait_angler_bait_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    bait_percentage = Column(String(8), nullable=False)


# noinspection SpellCheckingInspection
class FishCaughtCount(Fish):
    __tablename__ = 'fish_caught_count'

    fish_angler_fish_id = Column(ForeignKey('fish.fish_angler_fish_id'), primary_key=True)
    fish_caught_all_hours_count = Column(BigInteger, nullable=False)
    fish_caught_all_weathers_count = Column(BigInteger)


# noinspection SpellCheckingInspection
class FishCaughtPerHour(Base):
    __tablename__ = 'fish_caught_per_hour'

    fish_angler_fish_id = Column(ForeignKey('fish.fish_angler_fish_id'), primary_key=True, nullable=False)
    hour_num = Column(Integer, primary_key=True, nullable=False)
    hour_fish_caught_count = Column(BigInteger, nullable=False)

    fish_angler_fish = relationship('Fish')


# noinspection SpellCheckingInspection
class FishCaughtPerWeather(Base):
    __tablename__ = 'fish_caught_per_weather'

    fish_angler_fish_id = Column(ForeignKey('fish.fish_angler_fish_id'), primary_key=True, nullable=False)
    weather_name = Column(String(128), primary_key=True, nullable=False)
    weather_fish_caught_count = Column(BigInteger, nullable=False)

    fish_angler_fish = relationship('Fish')


# noinspection SpellCheckingInspection
class FishDesynthesisItem(Base):
    __tablename__ = 'fish_desynthesis_item'

    fish_angler_fish_id = Column(ForeignKey('fish.fish_angler_fish_id'), primary_key=True, nullable=False)
    desynthesis_item_id = Column(BigInteger, primary_key=True, nullable=False)
    desynthesis_item_name = Column(String(4096), nullable=False)
    desynthesis_icon_url = Column(String(2083), nullable=False)
    desynthesis_large_icon_url = Column(String(2083))
    desynthesis_angler_item_name = Column(String(4096), nullable=False)
    desynthesis_angler_lodestone_url = Column(String(2083))
    desynthesis_angler_percentage = Column(String(8), nullable=False)

    fish_angler_fish = relationship('Fish')


# noinspection SpellCheckingInspection
class FishInvolvedLeve(Base):
    __tablename__ = 'fish_involved_leve'

    fish_angler_fish_id = Column(ForeignKey('fish.fish_angler_fish_id'), primary_key=True, nullable=False, index=True)
    leve_id = Column(BigInteger, primary_key=True, nullable=False)
    leve_name = Column(String(4096), nullable=False)
    leve_angler_name = Column(String(4096), nullable=False)
    leve_angler_name_jp = Column(String(4096), nullable=False)
    leve_level = Column(SmallInteger, nullable=False)
    leve_angler_turn_in_count = Column(SmallInteger, nullable=False)

    fish_angler_fish = relationship('Fish')


# noinspection SpellCheckingInspection
class FishInvolvedRecipe(Base):
    __tablename__ = 'fish_involved_recipe'

    fish_angler_fish_id = Column(ForeignKey('fish.fish_angler_fish_id'), primary_key=True, nullable=False, index=True)
    recipe_item_id = Column(BigInteger, primary_key=True, nullable=False)
    recipe_item_name = Column(String(4096), nullable=False)
    recipe_angler_name = Column(String(4096), nullable=False)
    recipe_icon_url = Column(String(2083), nullable=False)
    recipe_large_icon_url = Column(String(2083))
    recipe_angler_lodestone_url = Column(String(2083))
    recipe_angler_crafting_class = Column(Text, nullable=False)

    fish_angler_fish = relationship('Fish')


# noinspection SpellCheckingInspection
class FishTugStrength(Base):
    __tablename__ = 'fish_tug_strength'

    fish_angler_fish_id = Column(ForeignKey('fish.fish_angler_fish_id'), primary_key=True, nullable=False, index=True)
    tug_strength = Column(Integer, primary_key=True, nullable=False)
    tug_strength_percent = Column(DECIMAL, nullable=False)

    fish_angler_fish = relationship('Fish')


# noinspection SpellCheckingInspection
class SpotAvailableFish(Base):
    __tablename__ = 'spot_available_fish'

    spot_angler_spot_id = Column(ForeignKey('spot.spot_angler_spot_id'), primary_key=True, nullable=False, index=True)
    fish_angler_fish_id = Column(ForeignKey('fish.fish_angler_fish_id'), primary_key=True, nullable=False, index=True)


# noinspection SpellCheckingInspection
class SpotBaitFishCatchInfo(Base):
    __tablename__ = 'spot_bait_fish_catch_info'

    spot_angler_spot_id = Column(ForeignKey('spot.spot_angler_spot_id'), primary_key=True, nullable=False, index=True)
    bait_angler_bait_id = Column(ForeignKey('bait.bait_angler_bait_id'), primary_key=True, nullable=False, index=True)
    fish_angler_fish_id = Column(ForeignKey('fish.fish_angler_fish_id'), primary_key=True, nullable=False, index=True)
    spot_bait_fish_catch_count = Column(BigInteger, nullable=False)
    spot_bait_fish_average_seconds_to_hook = Column(SmallInteger)
    spot_bait_fish_catch_percentage = Column(String(8), nullable=False)

    bait_angler_bait = relationship('Bait')
    fish_angler_fish = relationship('Fish')
    spot_angler_spot = relationship('Spot')


# noinspection SpellCheckingInspection
class SpotBaitTotalFishCaught(Base):
    __tablename__ = 'spot_bait_total_fish_caught'

    spot_angler_spot_id = Column(ForeignKey('spot.spot_angler_spot_id'), primary_key=True, nullable=False, index=True)
    bait_angler_bait_id = Column(ForeignKey('bait.bait_angler_bait_id'), primary_key=True, nullable=False, index=True)
    spot_bait_total_catch_count = Column(BigInteger, nullable=False)

    bait_angler_bait = relationship('Bait')
    spot_angler_spot = relationship('Spot')


# noinspection SpellCheckingInspection
class SpotEffectiveBait(Base):
    __tablename__ = 'spot_effective_bait'

    spot_angler_spot_id = Column(ForeignKey('spot.spot_angler_spot_id'), primary_key=True, nullable=False, index=True)
    bait_angler_bait_id = Column(ForeignKey('bait.bait_angler_bait_id'), primary_key=True, nullable=False, index=True)
