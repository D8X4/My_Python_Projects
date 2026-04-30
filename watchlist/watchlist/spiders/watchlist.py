
import scrapy

class BasicSpider(scrapy.Spider):
    name = 'watchlist'

    cookies = {
        # some sites might need cookies
        # aniwatch (rip) needed one
        }

    # Mapping based on your screenshots
    # 3 = Plan to Watch, 5 = Completed
    categories = {
        '3': 'Plan to Watch',
        '5': 'Completed'
    }

    def start_requests(self):
        for type_id, label in self.categories.items():
            url = f'https://aniwatchtv.to/user/watch-list?type={type_id}'
            yield scrapy.Request(
                url=url,
                cookies=self.cookies,
                meta={'category': label}
            )

    def parse(self, response):
        category = response.meta['category']
        
        for item in response.css('div.flw-item'):
            yield {
                'name': item.css('h3.film-name a::attr(title)').get(),
                'url': item.css('h3.film-name a::attr(href)').get(),
                'status': category 
            }

        # Pagination logic to keep the type_id consistent
        current_page = int(response.url.split('page=')[-1]) if 'page=' in response.url else 1
        if response.css(f'a.page-link[title="Page {current_page + 1}"]'):
            type_id = response.url.split('type=')[-1].split('&')[0]
            next_page = f'/user/watch-list?type={type_id}&page={current_page + 1}'
            yield response.follow(next_page, callback=self.parse, cookies=self.cookies, meta={'category': category})
