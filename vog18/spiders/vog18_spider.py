import urllib
import uuid
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.selector import Selector
from vog18.items import Vog18Item


class VOG18_Spider(CrawlSpider):
    page_name = 'page{0}.html'
    photo_name = 'photo{0}.jpg'
    xpath = '/html/body/div[3]/div[2]/div[2]/div/div[2]/div[3]/div[{0}]/div[2]/div[1]/div/a/img'
    attribute = '/@data-src_big'
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
        self.save_page(response.body)
        hxs = Selector(response)
        items = []
        for index in range(1, 11):
            elements = hxs.xpath(self.xpath.format(index) + self.attribute).extract()
            if len(elements) > 0:
                url = elements[0].split('|')[0]
                file_photo_name = self.photo_name.format(uuid.uuid4())
                urllib.urlretrieve(url, file_photo_name)
                item = Vog18Item()
                item['link'] = url
                item['photo_name'] = file_photo_name
                items.append(item)
        return items

    def save_page(self, content):
        with open(self.page_name.format(uuid.uuid4()), 'wb') as f:
            f.write(content)