""""defaults setting"""

# Mongodb
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
# Database
MONGODB_DB = "scrapy"

# For standalone use.
DUPEFILTER_KEY = "dupefilter:%(timestamp)s"

# Scheduler
SCHEDULER_PERSIST = False
SCHEDULER_QUEUE_TYPE = "FIFO"
SCHEDULER_QUEUE_KEY = "%(spider)s:requests"
SCHEDULER_QUEUE_CLASS = "scrapy_mongodb.queue.PriorityQueue"
SCHEDULER_DUPEFILTER_KEY = "%(spider)s:dupefilter"
SCHEDULER_DUPEFILTER_CLASS = "scrapy_mongodb.dupefilter.RFPDupeFilter"

# Items Pipeline
PIPELINE_KEY = "%(spider)s:items"

# Start urls
START_URLS_KEY = "%(name)s:start_urls"

# Stat
STATS_KEY = "%(spider)s:stats"

# Debug
MONGODB_DEBUG = False
