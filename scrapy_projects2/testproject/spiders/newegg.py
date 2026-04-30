import scrapy


class NeweggSpider(scrapy.Spider):
    name = "newegg"
    allowed_domains = ["www.newegg.com"]
    start_urls = ["https://www.newegg.com/Clearance-Store/EventSaleStore/ID-697?cm_sp=Head_Navigation-_-Under_Search_Bar-_-Clearance"]

    def parse(self, response):
        for item in response.css("#Product_List div.goods-container"):
            yield {
            "product_name": ''.join(item.css('a.goods-title::text').getall()).strip(),
            "price": ''.join(item.css('span.goods-price-value *::text').getall()),
            "link": item.css('a::attr(href)').get()
            }
        pass
