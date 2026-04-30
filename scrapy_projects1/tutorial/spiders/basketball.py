import scrapy


class BasketballSpider(scrapy.Spider):
    name = "basketball"
    allowed_domains = ["basketball-reference.com"]
    start_urls = ["https://basketball-reference.com/leagues/NBA_2025_standings.html"]

    def parse(self, response):
        for team in response.css("tr"):
            yield{
            "name": team.css("a::text").get(),
            "W": team.css('td[data-stat="wins"]::text').get(),
            "L": team.css('td[data-stat="wins"]::text').get()
            }
