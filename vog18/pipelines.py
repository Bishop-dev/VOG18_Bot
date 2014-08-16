import mimetypes
import gridfs
import pymongo
import requests

from scrapy.conf import settings
from scrapy import log


class VOG18(object):
    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.grid_fs = gridfs.GridFS(getattr(connection, settings['MONGODB_DB']))

    def process_item(self, item, spider):
        links = item['photos_links']
        ids = []
        for i, link in enumerate(links):
            mime_type = mimetypes.guess_type(link)[0]
            request = requests.get(link, stream=True)
            _id = self.grid_fs.put(request.raw, contentType=mime_type, filename=item['photo_names'][i])
            ids.append(_id)
        item['data_chunk_id'] = ids
        self.collection.insert(dict(item))
        log.msg("Item wrote to MongoDB database %s/%s" %
                (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                level=log.DEBUG, spider=spider)
        return item