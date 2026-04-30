import scrapy


class AotrSpider(scrapy.Spider):
    name = "aotr"
    allowed_domains = ["official-attack-on-titans-revolution.fandom.com"]
    start_urls = ["https://official-attack-on-titans-revolution.fandom.com/wiki/Codes"]

    def parse(self, response):
        for items in response.css('tr'):
            yield{
            "Code": item.css('td::text').get(),
            "rewards": item.css('td::text').get(),
            #"status": ,
            
            }
        pass
