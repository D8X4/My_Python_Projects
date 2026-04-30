import scrapy


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["en.wikipedia.org/wiki/List_of_most-followed_Instagram_accounts"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_most-followed_Instagram_accounts"]

    def parse(self, response):
        for account in response.css("tr"):
            yield{
            "account name:": account.css("a::text").get(),
            "followers:": account.css("td:nth-child(3)::text").get()
            }
