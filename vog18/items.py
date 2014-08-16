from scrapy.item import Item, Field


class Vog18Item(Item):
    photos_links = Field()
    photo_names = Field()
    post_link = Field()
    description = Field()
    data_chunk_id = Field()