import urllib
import uuid
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.selector import Selector


class VOG18_Spider(CrawlSpider):
    filename = 'page{0}.html'
    name = 'VOG18_spider'
    allowed_domains = ['vk.com']
    start_urls = ['https://m.vk.com/vog18']
    rules = [Rule
             (
                 SgmlLinkExtractor(restrict_xpaths=('//a[@class="show_more"]')),
                 callback='parse_public',
                 follow=True,
             )
    ]

    def parse_public(self, response):
        xpath = '/html/body/div[3]/div[2]/div[2]/div/div[2]/div[3]/div[{0}]/div[2]/div[1]/div/a/img'
        attribute = '/@data-src_big'
        self.save_page(response.body)
        hxs = Selector(response)
        for index in range(1, 11):
            elements = hxs.xpath(xpath.format(index) + attribute).extract()
            if len(elements) > 0:
                url = elements[0].split('|')[0]
                urllib.urlretrieve(url, 'photo{0}.jpg'.format(uuid.uuid4()))

    def save_page(self, content):
        with open(self.filename.format(uuid.uuid4()), 'wb') as f:
            f.write(content)