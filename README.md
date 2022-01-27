# Scrapy MongoDB

MongoDB-based components for Scrapy that allows distributed crawling

## Available Scrapy components

* Scheduler
* Duplication Filter

## Installation

From `github`

To install it via `pip`,

```bash
# install
pip install git+https://github.com/taicaile/scrapy-mongodb
# reinstall
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
pip install git+https://github.com/taicaile/scrapy-mongodb@v0.1.0
```

You can put the following in requirements.txt,

```bash
scrapy-mongodb@git+https://github.com/taicaile/scrapy-mongodb@v0.1.0
```

## Usage

Enable the components in your `settings.py`:

```python
# Enables scheduling storing requests queue in mongodb.
SCHEDULER = "scrapy_mongodb.scheduler.Scheduler"

# Specify the host and port to use when connecting to Mongodb (optional).
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = "scrapy"
```

Note this is not suitable for distribution currently.
