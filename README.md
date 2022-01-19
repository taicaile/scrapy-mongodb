# Scrapy MongoDB

MongoDB-based components for Scrapy that allows distributed crawling

## Available Scrapy components

* Scheduler
* Duplication Filter

## Installation

From `github`

To install it via `pip`,

```bash
pip install git+https://github.com/taicaile/scrapy-mongodb

pip install --ignore-installed git+https://github.com/taicaile/scrapy-mongodb
```

or clone it first,

```bash
git clone https://github.com/taicaile/scrapy-mongodb.git
cd scrapy-mongodb
python setup.py install
```

To install specific version,

```bash
# replace the version `v0.1.0` as you expect,
pip install git+https://github.com/taicaile/python-settings@v0.1.0
```

## Usage

Enable the components in your `settings.py`:

```python
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_mongodb.scheduler.Scheduler"

# Don't cleanup mongodb queues, allows to pause/resume crawls.
MONGODB_QUEUE_PERSIST = True

# Specify the host and port to use when connecting to Redis (optional).
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = "scrapy"
```
