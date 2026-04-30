import scrapy


class SoccerSpider(scrapy.Spider):
    name = "soccer"
    allowed_domains = ["adamchoi.com"]
    start_urls = ["https://adamchoi.com/opta/all"]

    def parse(self, response):
        pass
