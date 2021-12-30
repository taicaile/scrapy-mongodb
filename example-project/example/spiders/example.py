import scrapy
from scrapy.linkextractors import LinkExtractor


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["quotes.toscrape.com"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.link_extractor = LinkExtractor()

    def start_requests(self):
        urls = [
            "http://quotes.toscrape.com/page/1/",
            "http://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for link in self.link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)
