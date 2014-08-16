import urllib
import uuid
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from vog18.items import Vog18Item
from vog18.mongo_checker import MongoChecker


class VOG18_Spider(CrawlSpider):
    page_name = 'pages/page{0}.html'
    photo_name = 'photos/photo{0}.jpg'
    img_xpath0 = '//*[@id="mcont"]/div/div[2]/div[2]/div[{0}]/div[2]/div[1]/div/a/img/@data-src_big'
    img_xpath = '//*[@id="mcont"]/div/div[2]/div[3]/div[{0}]/div[2]/div[1]/div/a/img/@data-src_big'
    img_xpath_with_description = '//*[@id="mcont"]/div/div[2]/div[3]/div[{0}]/div[2]/div[2]/div/a/img/@data-src_big'

    description_xpath = '//*[@id="mcont"]/div/div[2]/div[3]/div[{0}]/div[2]/div[1]/text()'

    post_link_xpath0 = '//*[@id="mcont"]/div/div[2]/div[2]/div[{0}]/a/@name'
    post_link_xpath = '//*[@id="mcont"]/div/div[2]/div[3]/div[{0}]/a/@name'

    post_link_prefix = 'http://vk.com/vog18?w=wall-'

    pages_counter = 1
    counter_posts = 0
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
    mongo_checker = MongoChecker()

    def parse_start_url(self, response):
        # self.save_page(response.body)
        hxs = Selector(response)
        return self.parse_posts(hxs, 5, self.img_xpath0, self.post_link_xpath0)

    def parse_public(self, response):
        # self.save_page(response.body)
        hxs = Selector(response)
        return self.parse_posts(hxs, 10, self.img_xpath, self.post_link_xpath)

    def parse_posts(self, selector, amount, img_xpath, post_link_xpath):
        items = []
        for index in range(1, amount):
            # get post link and check if exists
            post_link = self.post_link_prefix + selector.xpath(post_link_xpath.format(index)).extract()[0].split('-')[1]
            if self.mongo_checker.check(post_link):
                raise CloseSpider('Shutdown. New posts: {0}'.format(self.counter_posts))

            # save images links and save it
            photos = selector.xpath(img_xpath.format(index)).extract()
            img_links = []
            photo_files_names = []
            for img in photos:
                img_link = img.split('|')[0]
                img_links.append(img_link)
                photo_file_name = self.photo_name.format(uuid.uuid4())
                try:
                    urllib.urlretrieve(img_link, photo_file_name)
                except Exception as e:
                    print e
                    import sys
                    sys.exit()
                photo_files_names.append(photo_file_name)

            # skip if there is no images
            if len(img_links) == 0:
                break

            # parse description
            description = selector.xpath(self.description_xpath.format(index)).extract()

            # save parsed information to item
            item = Vog18Item()
            item['photos_links'] = img_links
            item['photo_names'] = photo_files_names
            item['post_link'] = post_link
            if len(description) > 0:
                item['description'] = description[0]
            items.append(item)
            self.counter_posts += 1
            print item
        return items

    def save_page(self, content):
        # with open(self.page_name.format(uuid.uuid4()), 'wb') as f:
        with open(self.page_name.format(self.pages_counter), 'wb') as f:
            f.write(content)
        self.pages_counter += 1