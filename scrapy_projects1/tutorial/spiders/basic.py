import scrapy
from pathlib import Path

class BasicSpider(scrapy.Spider):
    name = "basic"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("a.tag::text").getall(),
            }
