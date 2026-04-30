import scrapy


class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_tallest_buildings"]

    def parse(self, response):
        for building in response.css("div.bodycount"):
            yield{
            "Name": building.css("a::attr(title)").get()
            #"Height": building.css("::text").get()
            }
