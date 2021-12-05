# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Ali1688Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_id=scrapy.Field()
    page_title = scrapy.Field()
    page_url = scrapy.Field()
    sku_props = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    sc_spid = scrapy.Field()
