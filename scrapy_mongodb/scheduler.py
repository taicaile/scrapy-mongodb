# -*- coding: utf-8 -*-
# (c) Lhassan Baazzi <baazzilhassan@gmail.com>

from scrapy.utils.misc import load_object

from . import connection, defaults
from .dupefilter import RFPDupeFilter


class Scheduler(object):
    def __init__(
        self,
        server,
        mongodb_db,
        persist,
        debug,
        queue_key=defaults.SCHEDULER_QUEUE_KEY,
        queue_cls=defaults.SCHEDULER_QUEUE_CLASS,
        dupefilter_key=defaults.SCHEDULER_DUPEFILTER_KEY,
        dupefilter_cls=defaults.SCHEDULER_DUPEFILTER_CLASS,
    ):
        self.server = server
        self.mongodb_db = mongodb_db
        self.persist = persist
        self.debug = debug
        self.queue_key = queue_key
        self.queue_cls = queue_cls
        self.dupefilter_key = dupefilter_key
        self.dupefilter_cls = dupefilter_cls

    @classmethod
    def from_settings(cls, settings):
        mongodb_db = settings.get("MONGODB_DB", defaults.MONGODB_DB)
        persist = settings.get("SCHEDULER_PERSIST", defaults.SCHEDULER_PERSIST)
        debug = settings.getbool("MONGODB_DEBUG", defaults.MONGODB_DEBUG)
        server = connection.from_settings(settings)

        return cls(server, mongodb_db, persist, debug)

    @classmethod
    def from_crawler(cls, crawler):
        instance = cls.from_settings(crawler.settings)
        # FIXME: for now, stats are only supported from this constructor
        instance.stats = crawler.stats
        return instance

    def open(self, spider):
        self.spider = spider
        self.db = self.server[self.mongodb_db]

        try:
            self.queue = load_object(self.queue_cls)(
                collection=self.db[self.queue_key % {"spider": spider.name}],
                spider=spider,
                key=self.queue_key % {"spider": spider.name},
            )
        except TypeError as e:
            raise ValueError(
                "Failed to instantiate queue class '%s': %s", self.queue_cls, e
            )

        self.df = RFPDupeFilter(
            self.db[self.dupefilter_key % {"spider": spider.name}],
            self.persist,
            self.debug,
        )

    def close(self, reason):
        if not self.persist:
            self.df.clear()
            self.queue.clear()

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False

        if self.stats:
            self.stats.inc_value("scheduler/enqueued/mongodb", spider=self.spider)

        self.queue.push(request)
        return True

    def next_request(self):

        request = self.queue.pop()

        if request and self.stats:
            self.stats.inc_value("scheduler/dequeued/mongodb", spider=self.spider)
        return request

    def has_pending_requests(self):
        return self.queue.__len__() > 0
