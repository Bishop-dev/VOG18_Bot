import pymongo
from scrapy.conf import settings


class MongoChecker():
    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def check(self, post_url):
        return self.collection.find({'post_link' : post_url}).count() > 0