#! /usr/bin/env python3

from ff14angler.apiServer.application import application

from gunicorn.app.base import BaseApplication


# noinspection PyAbstractClass
class GunicornWrapper(BaseApplication):

    def __init__(self, app):
        # noinspection SpellCheckingInspection,SpellCheckingInspection
        self._gunicorn_config = {
            'accesslog': '-',
            'error-file': '-',
            'bind': '0.0.0.0:9001',
            'keepalive': 2,
            'preload': True,
            'timeout': 30,
            'workers': 1,
            'log-level': 'debug',
            'access_log_format': '%(h)s %(l)s %(U)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %({Referer}i)s'
        }

        self.application = app
        super(GunicornWrapper, self).__init__()

    def load_config(self):
        for k, v in self._gunicorn_config.items():
            if k in self.cfg.settings and v is not None:
                self.cfg.set(k.casefold(), v)

    def load(self):
        return self.application


def main():
    GunicornWrapper(application).run()
