import scrapy
from pathlib import Path

class WorldstuffSpider(scrapy.Spider):
    name = "bookstuff"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css("article.product_pod"):
            yield {
            "title": book.css('h3 a::attr(title)').get(),
            "price": book.css('p.price_color::text').get()
            }
