import scrapy


class SpaceSpider(scrapy.Spider):
    name = "space"
    allowed_domains = ["https://www.scrapethissite.com/pages/simple/"]
    start_urls = ["https://www.worldometers.info/gdp/gdp-by-country/"]

    def parse(self, response):
        for money in response.css("tr"):
            yield {
            "Country": money.css("td:nth-child(2)::text").get(),
            "GDP": money.css("span.font-bold::text").get()
            }
