# -*- coding: utf-8 -*-
# (c) Lhassan Baazzi <baazzilhassan@gmail.com>

from pymongo import MongoClient

from . import defaults


def from_settings(settings):
    host = settings.get("MONGODB_SERVER", defaults.MONGODB_SERVER)
    port = settings.get("MONGODB_PORT", defaults.MONGODB_PORT)
    client = MongoClient(f"mongodb://{host}:{port}")
    client.server_info()
    return client
