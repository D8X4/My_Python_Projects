import scrapy


class DogeeSpider(scrapy.Spider):
    name = "dogee"
    allowed_domains = ["longdogechallenge.com"]
    start_urls = ["https://longdogechallenge.com"]

    def parse(self, response):
        for dog in response.css('div.wrapper'):
            yield{
            "hatted": dog.css('pre.hatted::text').get().replace('\n', ''),
            "head": dog.css('pre.head::text').get(),
            "neck": dog.css('pre.neck::text').get()
            }
