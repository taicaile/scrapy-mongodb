"""Scarpy MongoDB based Scheduler"""
import logging
import time

import pymongo.collection
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from . import connection, defaults

logger = logging.getLogger()


class RFPDupeFilter(BaseDupeFilter):
    """Mongodb-based request duplication filter"""

    def __init__(self, collection: "pymongo.collection.Collection", persist, debug):
        """Initialize the duplicates filter."""
        self.collection = collection
        self.persist = persist
        self.debug = debug
        self.stats = None
        self.spider = None
        self.create_index()

    def create_index(self):
        """create index for collection"""
        self.collection.create_index("fp")

    @classmethod
    def from_settings(cls, settings):
        mongodb_db = settings.get("MONGODB_DB", defaults.MONGODB_DB)
        dupefilter_key = settings.get(
            "MONGODB_DUPEFILTER_KEY", defaults.MONGODB_DUPEFILTER_KEY
        ) % {"timestamp": int(time.time())}

        server = connection.from_settings(settings)

        collection = server[mongodb_db][dupefilter_key]
        persist = settings.get(
            "MONGODB_DUPEFILTER_PERSIST", defaults.MONGODB_DUPEFILTER_PERSIST
        )
        debug = settings.getbool("MONGODB_DEBUG", defaults.MONGODB_DEBUG)

        return cls(collection, persist, debug)

    @classmethod
    def from_crawler(cls, crawler):
        """create cls from crawler"""
        return cls.from_settings(crawler.settings)

    @classmethod
    def from_spider(cls, spider):
        """create cls from spider"""

        settings = spider.settings
        server = connection.from_settings(settings)
        db_name = settings.get("MONGODB_DB", defaults.MONGODB_DB)
        dupefilter_key = settings.get(
            "MONGODB_SCHEDULER_DUPEFILTER_KEY",
            defaults.MONGODB_SCHEDULER_DUPEFILTER_KEY,
        ) % {"spider": spider.name}

        collection = server[db_name][dupefilter_key]
        persist = settings.get(
            "MONGODB_DUPEFILTER_PERSIST", defaults.MONGODB_DUPEFILTER_PERSIST
        )
        debug = settings.getbool("MONGODB_DEBUG", defaults.MONGODB_DEBUG)
        df = cls(collection, persist, debug)
        df.spider = spider
        return df

    def request_seen(self, request):
        fingerprint = request_fingerprint(request)
        result = self.collection.count_documents({"fp": fingerprint}, limit=1)
        if result == 0:
            self.collection.insert_one({"fp": fingerprint})
            return False

        if self.stats and self.spider:
            self.stats.inc_value("scheduler/dupefilter/mongodb", spider=self.spider)

        return True

    def close(self, reason):
        if not self.persist:
            self.clear()

    def clear(self):
        """Clear fingerprints data"""
        self.collection.drop()
