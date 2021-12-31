"""queue implemented based on mongodb"""
import datetime

import pymongo
import pymongo.collection
import scrapy  # pylint: disable=unused-import
from scrapy.utils.reqser import request_from_dict, request_to_dict

from . import astevaluate


class Base:
    """Per-spider base queue class"""

    sort = None

    def __init__(
        self,
        collection: "pymongo.collection.Collection",
        spider: "scrapy.Spider",
        key: str,
        serializer=None,
    ):
        """Initialize per-spider mongodb queue."""

        if serializer is None:
            # Backward compatibility.
            # TODO: deprecate pickle.
            serializer = astevaluate
        if not hasattr(serializer, "loads"):
            raise TypeError(
                f"serializer does not implement 'loads' function: {serializer}"
            )
        if not hasattr(serializer, "dumps"):
            raise TypeError(
                f"serializer does not implement 'dumps' function: {serializer}"
            )

        self.collection = collection
        self.spider = spider
        self.key = key % {"spider": spider.name}
        self.serializer = serializer
        # notice if there are requests already in the queue
        size = self.__len__()
        if size > 0:
            spider.log(f"Resuming crawl ({size} requests scheduled)")

        self.create_index()

    def create_index(self):
        if self.sort:
            self.collection.create_index(self.sort)

    def _encode_request(self, request):
        """Encode a request object"""
        obj = request_to_dict(request, self.spider)
        return self.serializer.dumps(obj)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        obj = self.serializer.loads(encoded_request)
        return request_from_dict(obj, self.spider)

    def __len__(self):
        """Return the length of the queue"""
        return self.collection.count_documents({})

    def push(self, request):
        """Push a request"""
        self.collection.insert_one(
            {
                "p": request.priority,
                "req": self._encode_request(request),
                "t": datetime.datetime.now(),
            }
        )

    def pop(self, timeout=0):
        """
        Pop a request
        timeout not support in this queue class
        """
        del timeout
        entry = self.collection.find_one_and_delete({}, sort=self.sort)
        if entry:
            request = self._decode_request(entry["req"])
            return request

        return None

    def clear(self):
        """Clear queue/stack"""
        self.collection.drop()


class PriorityQueue(Base):
    """Per-spider priority queue abstraction using redis' sorted set"""

    sort = [("p", pymongo.DESCENDING), ("t", pymongo.ASCENDING)]

    def create_index(self):
        self.collection.create_index(self.sort)


class LifoQueue(Base):
    """Last in first out"""

    sort = [("t", pymongo.DESCENDING)]


class FifoQueue(Base):
    """First in first out"""

    sort = [("t", pymongo.ASCENDING)]
