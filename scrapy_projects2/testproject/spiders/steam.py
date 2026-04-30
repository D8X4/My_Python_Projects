import scrapy


class SteamSpider(scrapy.Spider):
    name = "steam"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com/"]

    def parse(self, response):
        for item in response.css('a.tab_item'):
            name = item.css('div.tab_item_name::text').get()
            price = item.css('div.discount_final_price::text').get()
            if name:
                yield {
                    'name': name.strip(),
                    'price': price.strip() if price else 'Free'
                }