# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArxivSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    id = scrapy.Field()
    created = scrapy.Field()
    abstract = scrapy.Field()
    setSpec  = scrapy.Field()
    categories = scrapy.Field()
    authors = scrapy.Field()
    