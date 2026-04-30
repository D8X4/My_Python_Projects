import scrapy


class WorldclockSpider(scrapy.Spider):
    name = "worldclock"
    allowed_domains = ["timeanddate.com"]
    start_urls = ["https://timeanddate.com/worldclock"]

    def parse(self, response):
        for city in response.css("tr"):
            yield{
            "City:": city.css("a::text").get(),
            "time:": city.css("td::text").get()
            }
