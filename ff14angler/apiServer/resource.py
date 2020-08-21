#! /usr/bin/env python3

import json
import os

import falcon

from falconratelimit import rate_limit
from falcon import Request, Response
from falcon_autocrud.resource import CollectionResource
from sqlalchemy.orm.query import Query

from ff14angler.constants.values import SQLITE_DATABASE
from ff14angler.database import alchemyMapping


class RouteResource:

    def __init__(self, keys):
        self._keys = keys

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.body = json.dumps({'error': False, 'routes': self._keys})
        resp.content_type = 'application/json'
        resp.append_header('Vary', 'Accept')


class DataResource:

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.content_type = 'application/vnd.sqlite3'
        resp.stream = open(SQLITE_DATABASE, 'rb')
        resp.content_length = os.path.getsize(SQLITE_DATABASE)
        resp.downloadable_as = os.path.basename(SQLITE_DATABASE)


class LimitedCollectionResource(CollectionResource):

    allow_subresource = False

    @falcon.before(rate_limit(per_second=20, window_size=1))
    def on_get(self, req: Request, resp: Response, *args, **kwargs):
        return super().on_get(req, resp, *args, **kwargs)

    def get_filter(self, req: Request, resp: Response, query: Query, *args, **kwargs):
        limit = req.get_param_as_int('__limit')
        if not isinstance(limit, int) or limit > 100:
            req.params['__limit'] = 100
        return query.limit(limit)

    def after_get(self, req: Request, resp: Response, item: Query, *args, **kwargs):
        req.context['result']['error'] = False
        req.context['result']['meta']['total'] = item.limit(None).offset(None).count()
        req.context['result']['meta']['offset'] = req.context['result']['meta'].get('offset') or 0


class BaitCollectionResource(LimitedCollectionResource):
    methods = ['GET']
    model = alchemyMapping.Bait


class FishCollectionResource(LimitedCollectionResource):
    methods = ['GET']
    model = alchemyMapping.Fish


class SpotCollectionResource(LimitedCollectionResource):
    methods = ['GET']
    model = alchemyMapping.Spot


class CommentCollectionResource(LimitedCollectionResource):
    methods = ['GET']
    model = alchemyMapping.Comment
    naive_datetimes = ['comment_timestamp']


def _lookup_bait_comments_by_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Bait,
        alchemyMapping.BaitComment.bait_angler_bait_id == alchemyMapping.Bait.bait_angler_bait_id
    ).filter(alchemyMapping.Bait.bait_xivapi_item_id == kwargs['bait_xivapi_item_id'])


class BaitCommentCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {'bait_xivapi_item_id': _lookup_bait_comments_by_item_id}
    methods = ['GET']
    model = alchemyMapping.BaitComment
    naive_datetimes = ['comment_timestamp']


def _lookup_fish_comments_by_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Fish,
        alchemyMapping.FishComment.fish_angler_fish_id == alchemyMapping.Fish.fish_angler_fish_id
    ).filter(alchemyMapping.Fish.fish_xivapi_item_id == kwargs['fish_xivapi_item_id'])


class FishCommentCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {'fish_xivapi_item_id': _lookup_fish_comments_by_item_id}
    methods = ['GET']
    model = alchemyMapping.FishComment
    naive_datetimes = ['comment_timestamp']


def _lookup_spot_comment_by_spot_gathering_type(req: Request, resp: Response, query: Query, *args, **kwargs):
    if alchemyMapping.Spot not in [mapper.entity for mapper in query._join_entities]:
        query = query.join(
            alchemyMapping.Spot,
            alchemyMapping.SpotComment.spot_angler_spot_id == alchemyMapping.Spot.spot_angler_spot_id
        )
    return query.filter(alchemyMapping.Spot.spot_gathering_type == kwargs['spot_gathering_type'])


def _lookup_spot_comment_by_spot_gathering_type_unique_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    if alchemyMapping.Spot not in [mapper.entity for mapper in query._join_entities]:
        query = query.join(
            alchemyMapping.Spot,
            alchemyMapping.SpotComment.spot_angler_spot_id == alchemyMapping.Spot.spot_angler_spot_id
        )
    return query.filter(alchemyMapping.Spot.spot_gathering_type_unique_id == kwargs['spot_gathering_type_unique_id'])


class SpotCommentCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {
        'spot_gathering_type': _lookup_spot_comment_by_spot_gathering_type,
        'spot_gathering_type_unique_id': _lookup_spot_comment_by_spot_gathering_type_unique_id
    }
    methods = ['GET']
    model = alchemyMapping.SpotComment
    naive_datetimes = ['comment_timestamp']


def _lookup_bait_alt_currency_by_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Bait,
        alchemyMapping.BaitAltCurrencyPrice.bait_angler_bait_id == alchemyMapping.Bait.bait_angler_bait_id
    ).filter(alchemyMapping.Bait.bait_xivapi_item_id == kwargs['bait_xivapi_item_id'])


class BaitAltCurrencyPriceCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {'bait_xivapi_item_id': _lookup_bait_alt_currency_by_item_id}
    methods = ['GET']
    model = alchemyMapping.BaitAltCurrencyPrice


def _lookup_fish_bait_preference_by_bait_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Bait,
        alchemyMapping.FishBaitPreference.bait_angler_bait_id == alchemyMapping.Bait.bait_angler_bait_id
    ).filter(alchemyMapping.Bait.bait_xivapi_item_id == kwargs['bait_xivapi_item_id'])


def _lookup_fish_bait_preference_by_fish_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    query.join(
        alchemyMapping.Fish,
        alchemyMapping.FishBaitPreference.fish_angler_fish_id == alchemyMapping.Fish.fish_angler_fish_id
    ).filter(alchemyMapping.Fish.fish_angler_fish_id == kwargs['fish_xivapi_item_id'])


class FishBaitPreferenceCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {
        'bait_xivapi_item_id': _lookup_fish_bait_preference_by_fish_item_id,
        'fish_angler_fish_id': _lookup_fish_bait_preference_by_bait_item_id
    }
    methods = ['GET']
    model = alchemyMapping.FishBaitPreference


def _lookup_fish_caught_count_by_fish_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Fish,
        alchemyMapping.FishCaughtCount.fish_angler_fish_id == alchemyMapping.Fish.fish_angler_fish_id
    ).filter(alchemyMapping.Fish.fish_xivapi_item_id == kwargs['fish_xivapi_item_id'])


class FishCaughtCountCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {'fish_xivapi_item_id': _lookup_fish_caught_count_by_fish_item_id}
    methods = ['GET']
    model = alchemyMapping.FishCaughtCount


def _lookup_fish_caught_per_hour_by_fish_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Fish,
        alchemyMapping.FishCaughtPerHour.fish_angler_fish_id == alchemyMapping.Fish.fish_angler_fish_id
    ).filter(alchemyMapping.Fish.fish_xivapi_item_id == kwargs['fish_xivapi_item_id'])


class FishCaughtPerHourCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {'fish_xivapi_item_id': _lookup_fish_caught_per_hour_by_fish_item_id}
    methods = ['GET']
    model = alchemyMapping.FishCaughtPerHour


def _lookup_fish_caught_per_weather_by_fish_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Fish,
        alchemyMapping.FishCaughtPerWeather.fish_angler_fish_id == alchemyMapping.Fish.fish_angler_fish_id
    ).filter(alchemyMapping.Fish.fish_xivapi_item_id == kwargs['fish_xivapi_item_id'])


class FishCaughtPerWeatherCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {'fish_xivapi_item_id': _lookup_fish_caught_per_weather_by_fish_item_id}
    methods = ['GET']
    model = alchemyMapping.FishCaughtPerWeather


def _lookup_fish_desynthesis_item_by_fish_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Fish,
        alchemyMapping.FishDesynthesisItem.fish_angler_fish_id == alchemyMapping.Fish.fish_angler_fish_id
    ).filter(alchemyMapping.Fish.fish_xivapi_item_id == kwargs['fish_xivapi_item_id'])


class FishDesynthesisItemCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {'fish_xivapi_item_id': _lookup_fish_desynthesis_item_by_fish_item_id}
    methods = ['GET']
    model = alchemyMapping.FishDesynthesisItem


def _lookup_fish_involved_leve_by_fish_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Fish,
        alchemyMapping.FishInvolvedLeve.fish_angler_fish_id == alchemyMapping.Fish.fish_angler_fish_id
    ).filter(alchemyMapping.Fish.fish_xivapi_item_id == kwargs['fish_xivapi_item_id'])


class FishInvolvedLeveCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {'fish_xivapi_item_id': _lookup_fish_involved_leve_by_fish_item_id}
    methods = ['GET']
    model = alchemyMapping.FishInvolvedLeve


def _lookup_fish_involved_recipe_by_fish_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Fish,
        alchemyMapping.FishInvolvedRecipe.fish_angler_fish_id == alchemyMapping.Fish.fish_angler_fish_id
    ).filter(alchemyMapping.Fish.fish_xivapi_item_id == kwargs['fish_xivapi_item_id'])


class FishInvolvedRecipeCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {'fish_xivapi_item_id': _lookup_fish_involved_recipe_by_fish_item_id}
    methods = ['GET']
    model = alchemyMapping.FishInvolvedRecipe


def _lookup_fish_tug_strength_by_fish_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Fish,
        alchemyMapping.FishTugStrength.fish_angler_fish_id == alchemyMapping.Fish.fish_angler_fish_id
    ).filter(alchemyMapping.Fish.fish_xivapi_item_id == kwargs['fish_xivapi_item_id'])


class FishTugStrengthCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {'fish_xivapi_item_id': _lookup_fish_tug_strength_by_fish_item_id}
    methods = ['GET']
    model = alchemyMapping.FishTugStrength


def _lookup_spot_available_fish_by_fish_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Fish,
        alchemyMapping.SpotAvailableFish.fish_angler_fish_id == alchemyMapping.Fish.fish_angler_fish_id
    ).filter(alchemyMapping.Fish.fish_xivapi_item_id == kwargs['fish_xivapi_item_id'])


def _lookup_spot_available_fish_by_spot_gathering_type(req: Request, resp: Response, query: Query, *args, **kwargs):
    if alchemyMapping.Spot not in [mapper.entity for mapper in query._join_entities]:
        query = query.join(
            alchemyMapping.Spot,
            alchemyMapping.SpotAvailableFish.spot_angler_spot_id == alchemyMapping.Spot.spot_angler_spot_id
        )
    return query.filter(alchemyMapping.Spot.spot_gathering_type == kwargs['spot_gathering_type'])


def _lookup_spot_available_fish_by_spot_gathering_type_unique_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    if alchemyMapping.Spot not in [mapper.entity for mapper in query._join_entities]:
        query = query.join(
            alchemyMapping.Spot,
            alchemyMapping.SpotAvailableFish.spot_angler_spot_id == alchemyMapping.Spot.spot_angler_spot_id
        )
    return query.filter(alchemyMapping.Spot.spot_gathering_type_unique_id == kwargs['spot_gathering_type_unique_id'])


class SpotAvailableFishCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {
        'fish_xivapi_item_id': _lookup_spot_available_fish_by_fish_item_id,
        'spot_gathering_type': _lookup_spot_available_fish_by_spot_gathering_type,
        'spot_gathering_type_unique_id': _lookup_spot_available_fish_by_spot_gathering_type_unique_id,
    }

    methods = ['GET']
    model = alchemyMapping.SpotAvailableFish


def _lookup_spot_bait_fish_catch_info_by_bait_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Bait,
        alchemyMapping.SpotBaitFishCatchInfo.bait_angler_bait_id == alchemyMapping.Bait.bait_angler_bait_id
    ).filter(alchemyMapping.Bait.bait_xivapi_item_id == kwargs['bait_xivapi_item_id'])


def _lookup_spot_bait_fish_catch_info_by_fish_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Fish,
        alchemyMapping.SpotBaitFishCatchInfo.fish_angler_fish_id == alchemyMapping.Fish.fish_angler_fish_id
    ).filter(alchemyMapping.Fish.fish_xivapi_item_id == kwargs['fish_xivapi_item_id'])


def _lookup_spot_bait_fish_catch_info_by_spot_gathering_type(
    req: Request,
    resp: Response,
    query: Query,
    *args,
    **kwargs
):
    if alchemyMapping.Spot not in [mapper.entity for mapper in query._join_entities]:
        query = query.join(
            alchemyMapping.Spot,
            alchemyMapping.SpotBaitFishCatchInfo.spot_angler_spot_id == alchemyMapping.Spot.spot_angler_spot_id
        )
    return query.filter(alchemyMapping.Spot.spot_gathering_type == kwargs['spot_gathering_type'])


def _lookup_spot_bait_fish_catch_info_by_spot_gathering_type_unique_id(
    req: Request,
    resp: Response,
    query: Query,
    *args,
    **kwargs
):
    if alchemyMapping.Spot not in [mapper.entity for mapper in query._join_entities]:
        query = query.join(
            alchemyMapping.Spot,
            alchemyMapping.SpotBaitFishCatchInfo.spot_angler_spot_id == alchemyMapping.Spot.spot_angler_spot_id
        )
    return query.filter(alchemyMapping.Spot.spot_gathering_type_unique_id == kwargs['spot_gathering_type_unique_id'])


class SpotBaitFishCatchInfoCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {
        'bait_xivapi_item_id': _lookup_spot_bait_fish_catch_info_by_bait_item_id,
        'fish_xivapi_item_id': _lookup_spot_bait_fish_catch_info_by_fish_item_id,
        'spot_gathering_type': _lookup_spot_bait_fish_catch_info_by_spot_gathering_type,
        'spot_gathering_type_unique_id': _lookup_spot_bait_fish_catch_info_by_spot_gathering_type_unique_id
    }

    methods = ['GET']
    model = alchemyMapping.SpotBaitFishCatchInfo


def _lookup_spot_bait_total_fish_caught_by_bait_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Bait,
        alchemyMapping.SpotBaitTotalFishCaught.bait_angler_bait_id == alchemyMapping.Bait.bait_angler_bait_id
    ).filter(alchemyMapping.Bait.bait_xivapi_item_id == kwargs['bait_xivapi_item_id'])


def _lookup_spot_bait_total_fish_caught_by_spot_gathering_type(
    req: Request,
    resp: Response,
    query: Query,
    *args,
    **kwargs
):
    if alchemyMapping.Spot not in [mapper.entity for mapper in query._join_entities]:
        query = query.join(
            alchemyMapping.Spot,
            alchemyMapping.SpotBaitTotalFishCaught.spot_angler_spot_id == alchemyMapping.Spot.spot_angler_spot_id
        )
    return query.filter(alchemyMapping.Spot.spot_gathering_type == kwargs['spot_gathering_type'])


def _lookup_spot_bait_total_fish_caught_by_spot_gathering_type_unique_id(
    req: Request,
    resp: Response,
    query: Query,
    *args,
    **kwargs
):
    if alchemyMapping.Spot not in [mapper.entity for mapper in query._join_entities]:
        query = query.join(
            alchemyMapping.Spot,
            alchemyMapping.SpotBaitTotalFishCaught.spot_angler_spot_id == alchemyMapping.Spot.spot_angler_spot_id
        )
    return query.filter(alchemyMapping.Spot.spot_gathering_type_unique_id == kwargs['spot_gathering_type_unique_id'])


class SpotBaitTotalFishCaughtCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {
        'bait_xivapi_item_id': _lookup_spot_bait_total_fish_caught_by_bait_item_id,
        'spot_gathering_type': _lookup_spot_bait_total_fish_caught_by_spot_gathering_type,
        'spot_gathering_type_unique_id': _lookup_spot_bait_total_fish_caught_by_spot_gathering_type_unique_id
    }
    methods = ['GET']
    model = alchemyMapping.SpotBaitTotalFishCaught


def _lookup_spot_effective_bait_by_bait_item_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    return query.join(
        alchemyMapping.Bait,
        alchemyMapping.SpotEffectiveBait.bait_angler_bait_id == alchemyMapping.Bait.bait_angler_bait_id
    ).filter(alchemyMapping.Bait.bait_xivapi_item_id == kwargs['bait_xivapi_item_id'])


def _lookup_spot_effective_bait_by_spot_gathering_type(req: Request, resp: Response, query: Query, *args, **kwargs):
    if alchemyMapping.Spot not in [mapper.entity for mapper in query._join_entities]:
        query = query.join(
            alchemyMapping.Spot,
            alchemyMapping.SpotEffectiveBait.spot_angler_spot_id == alchemyMapping.Spot.spot_angler_spot_id
        )
    return query.filter(alchemyMapping.Spot.spot_gathering_type == kwargs['spot_gathering_type'])


def _lookup_spot_effective_bait_by_spot_gathering_type_unique_id(req: Request, resp: Response, query: Query, *args, **kwargs):
    if alchemyMapping.Spot not in [mapper.entity for mapper in query._join_entities]:
        query = query.join(
            alchemyMapping.Spot,
            alchemyMapping.SpotEffectiveBait.spot_angler_spot_id == alchemyMapping.Spot.spot_angler_spot_id
        )
    return query.filter(alchemyMapping.Spot.spot_gathering_type_unique_id == kwargs['spot_gathering_type_unique_id'])


class SpotEffectiveBaitCollectionResource(LimitedCollectionResource):
    lookup_attr_map = {
        'bait_xivapi_item_id': _lookup_spot_effective_bait_by_bait_item_id,
        'spot_gathering_type': _lookup_spot_effective_bait_by_spot_gathering_type,
        'spot_gathering_type_unique_id': _lookup_spot_effective_bait_by_spot_gathering_type_unique_id
    }

    methods = ['GET']
    model = alchemyMapping.SpotEffectiveBait
