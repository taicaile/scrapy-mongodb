"""Scarpy MongoDB Scheduler"""

import pymongo
from scrapy.utils.misc import load_object

from . import connection, defaults


class Scheduler:
    """Scarpy Scheduler"""

    # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        server,
        db_name,
        persist,
        debug,
    ):
        self.server: "pymongo.MongoClient" = server
        self.db_name = db_name
        self.persist = persist
        self.debug = debug
        self.queue_key = defaults.SCHEDULER_QUEUE_KEY
        self.queue_cls = defaults.SCHEDULER_QUEUE_CLASS
        self.dupefilter_key = defaults.SCHEDULER_DUPEFILTER_KEY
        self.dupefilter_cls = defaults.SCHEDULER_DUPEFILTER_CLASS

        # for open
        self.spider = None
        self.queue = None
        self.df = None
        self.stats = None

    @classmethod
    def from_settings(cls, settings):
        """create cls from settings"""
        server = connection.from_settings(settings)
        db_name = settings.get("MONGODB_DB", defaults.MONGODB_DB)
        persist = settings.get("SCHEDULER_PERSIST", defaults.SCHEDULER_PERSIST)
        debug = settings.getbool("MONGODB_DEBUG", defaults.MONGODB_DEBUG)

        return cls(server, db_name, persist, debug)

    @classmethod
    def from_crawler(cls, crawler):
        """create from crawler"""
        instance = cls.from_settings(crawler.settings)
        # FIXME: for now, stats are only supported from this constructor
        instance.stats = crawler.stats
        return instance

    def open(self, spider):
        """spider open"""
        self.spider = spider
        db = self.server[self.db_name]

        try:
            self.queue = load_object(self.queue_cls)(
                collection=db[self.queue_key % {"spider": spider.name}],
                spider=spider,
                key=self.queue_key % {"spider": spider.name},
            )
        except TypeError as e:
            raise ValueError(
                f"Failed to instantiate queue class '{self.queue_cls}': {e}"
            ) from e

        self.df = load_object(self.dupefilter_cls).from_spider(spider)
        if self.stats:
            self.df.stats = self.stats

    def close(self, reason):
        """spider close"""
        del reason
        if not self.persist:
            self.df.clear()
            self.queue.clear()

    def enqueue_request(self, request):
        """enqueue_request"""
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False

        if self.stats:
            self.stats.inc_value("scheduler/enqueued/mongodb", spider=self.spider)

        self.queue.push(request)
        return True

    def next_request(self):
        """get next request from queue"""
        request = self.queue.pop()

        if request and self.stats:
            self.stats.inc_value("scheduler/dequeued/mongodb", spider=self.spider)
        return request

    def has_pending_requests(self):
        """has_pending_requests"""
        return self.queue.__len__() > 0
