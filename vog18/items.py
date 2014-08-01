from scrapy.item import Item, Field


class Vog18Item(Item):
    link = Field()
    photo_name = Field()