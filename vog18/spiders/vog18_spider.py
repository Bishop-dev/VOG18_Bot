from scrapy.contrib.spiders.crawl import CrawlSpider
from scrapy.selector import Selector


class VOG18_Spider(CrawlSpider):
    filename = 'page.html'
    name = 'VOG18_spider'
    allowed_domains = ['vk.com', 'pp.vk.me']
    start_urls = ['https://m.vk.com/vog18']

    def parse(self, response):
        xpath = "/html/body/div[3]/div[2]/div[2]/div/div[2]/div[2]/div[{0}]/div[2]/div[1]/div/a/img"
        hxs = Selector(response)
        self.save_page(response.body)
        for x in range(1, 6):
            print(hxs.xpath(xpath.format(x) + '/@data-src_big').extract())

    def save_page(self, content):
        with open(self.filename, 'wb') as f:
            f.write(content)