import scrapy


class CompanySpider(scrapy.Spider):
    name = "company"
    allowed_domains = ["opencorporates.com"]
    start_urls = ["https://opencorporates.com/companies/us_ca"]

    def parse(self, response):
        pass
