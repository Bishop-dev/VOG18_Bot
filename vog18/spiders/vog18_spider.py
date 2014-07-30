from scrapy.contrib.spiders.crawl import CrawlSpider


class VOG18_Spider(CrawlSpider):
    name = 'VOG18_spider'
    allowed_domains = ['vk.com', 'pp.vk.me']
    start_urls = ['https://m.vk.com/vog18']

    def parse(self, response):
        with open('filename.html', 'wb') as f:
            f.write(response.body)