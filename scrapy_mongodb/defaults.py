""""defaults setting"""

# Mongodb
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
# Database
MONGODB_DB = "scrapy"

# For standalone use.
MONGODB_DUPEFILTER_KEY = "dupefilter:%(timestamp)s"

# Duplifiter
MONGODB_DUPEFILTER_PERSIST = False
# Scheduler
MONGODB_SCHEDULER_QUEUE_PERSIST = False
MONGODB_SCHEDULER_QUEUE_KEY = "%(spider)s:requests"
MONGODB_SCHEDULER_QUEUE_CLASS = "scrapy_mongodb.queue.FifoQueue"
MONGODB_SCHEDULER_DUPEFILTER_KEY = "%(spider)s:dupefilter"
MONGODB_SCHEDULER_DUPEFILTER_CLASS = "scrapy_mongodb.dupefilter.RFPDupeFilter"

# Items Pipeline
MONGODB_PIPELINE_KEY = "%(spider)s:items:%(item)s"

# Start urls
MONGODB_START_URLS_KEY = "%(name)s:start_urls"

# Stat
MONGODB_STATS_KEY = "%(spider)s:stats"

# Debug
MONGODB_DEBUG = False
