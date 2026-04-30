from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "facts"

    async def start(self):
        urls = [
            "https://en.wikipedia.org/wiki/Plumed_whistling_duck",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"article-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")