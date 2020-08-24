#! /usr/bin/env python3

import falcon

from falcon_autocrud.middleware import Middleware
from sqlalchemy import create_engine

from ff14angler.apiServer.corsMiddleware import CorsMiddleware
from ff14angler.apiServer.route import register_routes
from ff14angler.constants.values import SQLITE_DATABASE


db_engine = create_engine('sqlite:///{}'.format(SQLITE_DATABASE))
application = falcon.API(middleware=[CorsMiddleware(), Middleware()])
register_routes(application, db_engine)
