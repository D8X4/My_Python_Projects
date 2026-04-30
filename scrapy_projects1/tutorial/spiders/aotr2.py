import scrapy


class Aotr2Spider(scrapy.Spider):
    name = "aotr2"
    allowed_domains = ["beebom.com/attack-on-titan-revolution-aotr-codes/"]
    start_urls = ['https://beebom.com/attack-on-titan-revolution-aotr-codes/']

    def parse(self, response):
        for codes in response.css('li'):
            yield{
            "code": codes.css('strong::text').get(),
            #"rewards": codes.css('strong::text').get()[1],
            #"status": 
            }
        pass
