"""MongoDB Item Pipeline"""
from scrapy.utils.misc import load_object
from twisted.internet.threads import deferToThread

from . import connection, defaults


class MongoDBPipeline:
    """Pushes serialized item into a MongoDB collection"""

    def __init__(self, server, db_name, key):
        """Initialize pipeline."""
        self.server = server
        self.db_name = db_name
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        """create from settings"""
        params = {
            "server": connection.from_settings(settings),
            "db_name": settings.get("MONGODB_DB", defaults.MONGODB_DB),
            "key": settings.get(
                "MONGODB_ITEMS_PIPELINE_KEY", defaults.MONGODB_PIPELINE_KEY
            ),
        }

        if settings.get("REDIS_ITEMS_SERIALIZER"):
            params["serialize_func"] = load_object(settings["REDIS_ITEMS_SERIALIZER"])

        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        """create from crawler"""
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        """process item"""
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        """process item"""
        # pylint:disable=protected-access
        key = self.item_key(item, spider)
        data = item._values
        self.server[self.db_name][key].insert_one(data)
        return item

    def item_key(self, item, spider):
        """Returns mongodb key based on given spider."""
        return self.key % {"spider": spider.name, "item": item.__class__.__name__}
