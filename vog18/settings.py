BOT_NAME = 'vog18'

SPIDER_MODULES = ['vog18.spiders']
NEWSPIDER_MODULE = 'vog18.spiders'

ITEM_PIPELINES = ['vog18.pipelines.VOG18',]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "vog18"
MONGODB_COLLECTION = "vog18_photos"
