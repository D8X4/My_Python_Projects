import scrapy

class WalmartSpider(scrapy.Spider):
    name = "walmart"
    allowed_domains = ["walmart.com"]
    start_urls = ["https://www.walmart.com/cp/video-games/2636?povid=GlobalNav_rWeb_ETS_gamingentertainment_consolesbundles"]

    def parse(self, response):
        for item in response.css('div[role="group"]'):
            title = item.css('span[data-automation-id="product-title"]::text').get()
            price = item.css('div[data-automation-id="product-price"] span.ld_FS::text').get()
            
            if title:  # skip items without a title
                yield {
                    "title": title,
                    "price": price.replace("current price ", "").strip() if price else None,
                }
        next_page = response.css('a[data-testid="NextPage"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)