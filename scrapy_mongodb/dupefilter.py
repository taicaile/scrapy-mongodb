"""Scarpy MongoDB based Scheduler"""
import logging
import time

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from . import connection, defaults

logger = logging.getLogger()


class RFPDupeFilter(BaseDupeFilter):
    """Mongodb-based request duplication filter"""

    def __init__(self, collection, persist, debug):
        """Initialize the duplicates filter."""
        self.collection = collection
        self.persist = persist
        self.debug = debug

    @classmethod
    def from_settings(cls, settings):
        mongodb_db = settings.get("MONGODB_DB", defaults.MONGODB_DB)
        dupefilter_key = settings.get("DUPEFILTER_KEY", defaults.DUPEFILTER_KEY) % {
            "timestamp": int(time.time())
        }

        server = connection.from_settings(settings)

        collection = server[mongodb_db][dupefilter_key]
        persist = settings.get("SCHEDULER_PERSIST", defaults.SCHEDULER_PERSIST)
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
            "SCHEDULER_DUPEFILTER_KEY", defaults.SCHEDULER_DUPEFILTER_KEY
        ) % {"spider": spider.name}

        collection = server[db_name][dupefilter_key]
        persist = settings.get("SCHEDULER_PERSIST", defaults.SCHEDULER_PERSIST)
        debug = settings.getbool("MONGODB_DEBUG", defaults.MONGODB_DEBUG)
        return cls(collection, persist, debug)

    def request_seen(self, request):
        fingerprint = request_fingerprint(request)
        result = self.collection.find_one({"_id": fingerprint})
        if not result:
            self.collection.insert_one({"_id": fingerprint})
            return False

        return True

    def close(self, reason):
        if not self.persist:
            self.clear()

    def clear(self):
        """Clears fingerprints data"""
        self.collection.drop()
