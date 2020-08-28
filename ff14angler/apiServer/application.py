#! /usr/bin/env python3

import falcon

from falcon_autocrud.middleware import Middleware
from falcon_sslify import FalconSSLify
from sqlalchemy import create_engine

from ff14angler.apiServer.corsMiddleware import CorsMiddleware
from ff14angler.apiServer.route import register_routes
from ff14angler.constants.values import DEBUG_SERVER, SQLITE_DATABASE


if DEBUG_SERVER:
    middleware = [CorsMiddleware(), Middleware()]
else:
    middleware = [FalconSSLify(), CorsMiddleware(), Middleware()]

db_engine = create_engine('sqlite:///{}'.format(SQLITE_DATABASE))
application = falcon.API(middleware=middleware)
register_routes(application, db_engine)
