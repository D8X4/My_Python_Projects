import scrapy


class StatsSpider(scrapy.Spider):
    name = "stats"
    allowed_domains = ["scrapethissite.com"]
    start_urls = ["https://scrapethissite.com/pages/forms"]

    def parse(self, response):
        for team in response.css("tr"):
            if team.css("td.name"):
                yield{
                "name": team.css("td.name::text").get().strip(),
                "year": team.css("td.year::text").get().strip(),
                "wins": team.css("td.wins::text").get().strip(),
                "losses": team.css("td.losses::text").get().strip()
                }
