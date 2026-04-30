import scrapy


class CrawlSpider(scrapy.Spider):
    name = "typestats"
    allowed_domains = ["play.typeracer.com"]
    start_urls = ["https://play.typeracer.com/"]

    def parse(self, response):
        pass
