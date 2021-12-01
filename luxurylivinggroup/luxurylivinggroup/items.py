# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LuxurylivinggroupItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    title = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    desc = scrapy.Field()
    page_url = scrapy.Field()
    brand_name = scrapy.Field()
    brand_url = scrapy.Field()
