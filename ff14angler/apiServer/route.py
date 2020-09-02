#! /usr/bin/env python3

import json

import falcon

from typing import Dict, Type

from sqlalchemy.engine.base import Engine

from ff14angler.apiServer import resource


# noinspection PyUnusedLocal
def handle_404(req: falcon.Request, resp: falcon.Response):
    resp.status = falcon.HTTP_404
    resp.body = json.dumps(
        {
            'error': True,
            'message': 'Page not found.',
            'reason': 404,
        }
    )


# noinspection PyUnusedLocal
def json_error_serializer(req: falcon.Request, resp: falcon.Response, exception: falcon.HTTPError):
    resp.body = json.dumps({'error': True, 'message': exception.title, 'reason': exception.status})
    resp.content_type = 'application/json'
    resp.append_header('Vary', 'Accept')


def register_routes(app: falcon.API, db_engine: Engine):
    app.add_sink(handle_404, '')
    app.set_error_serializer(json_error_serializer)

    routes: Dict[str, Type[resource.LimitedCollectionResource]] = {
        '/bait': resource.BaitCollectionResource,
        '/bait/angler_id/{bait_angler_bait_id}': resource.BaitCollectionResource,
        '/bait/item_id/{bait_xivapi_item_id}': resource.BaitCollectionResource,
        '/bait/name/{name}': resource.BaitCollectionResource,
        '/fish': resource.FishCollectionResource,
        '/fish/angler_id/{fish_angler_fish_id}': resource.FishCollectionResource,
        '/fish/item_id/{fish_xivapi_item_id}': resource.FishCollectionResource,
        '/fish/name/{name}': resource.FishCollectionResource,
        '/spot': resource.SpotCollectionResource,
        '/spot/angler_id/{spot_angler_spot_id}': resource.SpotCollectionResource,
        '/spot/{spot_gathering_type}/{spot_gathering_type_unique_id}': resource.SpotCollectionResource,
        '/spot/name/{name}': resource.SpotCollectionResource,
        '/comment': resource.CommentCollectionResource,
        '/comment/bait': resource.BaitCommentCollectionResource,
        '/comment/bait/angler_id/{bait_angler_bait_id}': resource.BaitCommentCollectionResource,
        '/comment/bait/item_id/{bait_xivapi_item_id}': resource.BaitCommentCollectionResource,
        '/comment/fish': resource.FishCommentCollectionResource,
        '/comment/fish/angler_id/{fish_angler_fish_id}': resource.FishCommentCollectionResource,
        '/comment/fish/item_id/{fish_xivapi_item_id}': resource.FishCommentCollectionResource,
        '/comment/spot': resource.SpotCommentCollectionResource,
        '/comment/spot/angler_id/{spot_angler_spot_id}': resource.SpotCommentCollectionResource,
        '/comment/spot/{spot_gathering_type}/{spot_gathering_type_unique_id}': resource.SpotCommentCollectionResource,
        '/bait_alt_currency': resource.BaitAltCurrencyPriceCollectionResource,
        '/bait_alt_currency/angler_id/{bait_angler_bait_id}': resource.BaitAltCurrencyPriceCollectionResource,
        '/bait_alt_currency/item_id/{bait_xivapi_item_id}': resource.BaitAltCurrencyPriceCollectionResource,
        '/fish_bait_preference': resource.FishBaitPreferenceCollectionResource,
        '/fish_bait_preference/bait/angler_id/{bait_angler_bait_id}': resource.FishBaitPreferenceCollectionResource,
        '/fish_bait_preference/bait/item_id/{bait_xivapi_item_id}': resource.FishBaitPreferenceCollectionResource,
        '/fish_bait_preference/fish/angler_id/{fish_angler_fish_id}': resource.FishBaitPreferenceCollectionResource,
        '/fish_bait_preference/fish/item_id/{fish_xivapi_item_id}': resource.FishBaitPreferenceCollectionResource,
        '/fish_caught_count': resource.FishCaughtCountCollectionResource,
        '/fish_caught_count/angler_id/{fish_angler_fish_id}': resource.FishCaughtCountCollectionResource,
        '/fish_caught_count/item_id/{fish_xivapi_item_id}': resource.FishCaughtCountCollectionResource,
        '/fish_caught_per_hour': resource.FishCaughtPerHourCollectionResource,
        '/fish_caught_per_hour/angler_id/{fish_angler_fish_id}': resource.FishCaughtPerHourCollectionResource,
        '/fish_caught_per_hour/item_id/{fish_xivapi_item_id}': resource.FishCaughtPerHourCollectionResource,
        '/fish_caught_per_weather': resource.FishCaughtPerWeatherCollectionResource,
        '/fish_caught_per_weather/angler_id/{fish_angler_fish_id}': resource.FishCaughtPerWeatherCollectionResource,
        '/fish_caught_per_weather/item_id/{fish_xivapi_item_id}': resource.FishCaughtPerWeatherCollectionResource,
        '/fish_desynthesis_item': resource.FishDesynthesisItemCollectionResource,
        '/fish_desynthesis_item/angler_id/{fish_angler_fish_id}': resource.FishDesynthesisItemCollectionResource,
        '/fish_desynthesis_item/item_id/{fish_xivapi_item_id}': resource.FishDesynthesisItemCollectionResource,
        '/fish_involved_leve': resource.FishInvolvedLeveCollectionResource,
        '/fish_involved_leve/angler_id/{fish_angler_fish_id}': resource.FishInvolvedLeveCollectionResource,
        '/fish_involved_leve/item_id/{fish_xivapi_item_id}': resource.FishInvolvedLeveCollectionResource,
        '/fish_involved_recipe': resource.FishInvolvedRecipeCollectionResource,
        '/fish_involved_recipe/angler_id/{fish_angler_fish_id}': resource.FishInvolvedRecipeCollectionResource,
        '/fish_involved_recipe/item_id/{fish_xivapi_item_id}': resource.FishInvolvedRecipeCollectionResource,
        '/fish_tug_strength': resource.FishTugStrengthCollectionResource,
        '/fish_tug_strength/angler_id/{fish_angler_fish_id}': resource.FishTugStrengthCollectionResource,
        '/fish_tug_strength/item_id/{fish_xivapi_item_id}': resource.FishTugStrengthCollectionResource,
        '/spot_available_fish': resource.SpotAvailableFishCollectionResource,
        '/spot_available_fish/fish/angler_id/{fish_angler_fish_id}': resource.SpotAvailableFishCollectionResource,
        '/spot_available_fish/fish/item_id/{fish_xivapi_item_id}': resource.SpotAvailableFishCollectionResource,
        '/spot_available_fish/spot/angler_id/{spot_angler_spot_id}': resource.SpotAvailableFishCollectionResource,
        '/spot_available_fish/spot/{spot_gathering_type}/{spot_gathering_type_unique_id}': (
            resource.SpotAvailableFishCollectionResource
        ),
        '/spot_bait_fish_catch_info': resource.SpotBaitFishCatchInfoCollectionResource,
        '/spot_bait_fish_catch_info/bait/angler_id/{bait_angler_bait_id}': (
            resource.SpotBaitFishCatchInfoCollectionResource
        ),
        '/spot_bait_fish_catch_info/bait/item_id/{bait_xivapi_item_id}': (
            resource.SpotBaitFishCatchInfoCollectionResource
        ),
        '/spot_bait_fish_catch_info/fish/angler_id/{fish_angler_fish_id}': (
            resource.SpotBaitFishCatchInfoCollectionResource
        ),
        '/spot_bait_fish_catch_info/fish/item_id/{fish_xivapi_item_id}': (
            resource.SpotBaitFishCatchInfoCollectionResource
        ),
        '/spot_bait_fish_catch_info/spot/angler_id/{spot_angler_spot_id}': (
            resource.SpotBaitFishCatchInfoCollectionResource
        ),
        '/spot_bait_fish_catch_info/spot/{spot_gathering_type}/{spot_gathering_type_unique_id}': (
            resource.SpotBaitFishCatchInfoCollectionResource
        ),
        '/spot_bait_total_fish_caught': resource.SpotBaitTotalFishCaughtCollectionResource,
        '/spot_bait_total_fish_caught/bait/angler_id/{bait_angler_bait_id}': (
            resource.SpotBaitTotalFishCaughtCollectionResource
        ),
        '/spot_bait_total_fish_caught/bait/item_id/{bait_xivapi_item_id}': (
            resource.SpotBaitTotalFishCaughtCollectionResource
        ),
        '/spot_bait_total_fish_caught/spot/angler_id/{spot_angler_spot_id}': (
            resource.SpotBaitTotalFishCaughtCollectionResource
        ),
        '/spot_bait_total_fish_caught/spot/{spot_gathering_type}/{spot_gathering_type_unique_id}': (
            resource.SpotBaitTotalFishCaughtCollectionResource
        ),
        '/spot_effective_bait': resource.SpotEffectiveBaitCollectionResource,
        '/spot_effective_bait/bait/angler_id/{bait_angler_bait_id}': (
            resource.SpotEffectiveBaitCollectionResource
        ),
        '/spot_effective_bait/bait/item_id/{bait_xivapi_item_id}': (
            resource.SpotEffectiveBaitCollectionResource
        ),
        '/spot_effective_bait/spot/angler_id/{spot_angler_spot_id}': (
            resource.SpotEffectiveBaitCollectionResource
        ),
        '/spot_effective_bait/spot/{spot_gathering_type}/{spot_gathering_type_unique_id}': (
            resource.SpotEffectiveBaitCollectionResource
        ),
        '/last_updated': resource.LastUpdatedCollectionResource
    }

    app.add_route('/', resource.RouteResource(list(routes.keys())))
    app.add_route('/db', resource.DataResource())

    for route_uri, collection in routes.items():
        app.add_route(route_uri, collection(db_engine))
