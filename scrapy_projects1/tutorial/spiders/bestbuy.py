import scrapy


class BestbuySpider(scrapy.Spider):
    name = "bestbuy"
    allowed_domains = ["www.bestbuy.com"]
    start_urls = ["https://www.bestbuy.com/site/misc/deal-of-the-day/pcmcat248000050016.c?id=pcmcat248000050016"]

    def parse(self, response):
        for item in response.css('div.wf-offer-content.col-xs-7'):
            yield{
            "site" : response.css('title::text').get(),
            "name: ": item.css('a.wf-offer-link.v-line-clamp::text').get(),
            "time_left": response.css('div.sr-only.sale-timer::text').get()
            }
        pass
