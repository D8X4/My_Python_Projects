import scrapy

class RedditSpider(scrapy.Spider):
    name = "thissite"
    allowed_domains = ["scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/simple"]

    def parse(self, response):
        for name in response.css('div.country'):
            yield{
            "name": name.css("h3.country-name::text").getall()[-1].strip(),
            "info": name.css("span.country-population::text").get()
            }
