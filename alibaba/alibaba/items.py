# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlibabaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DetailItem(scrapy.Item):
    abtest = scrapy.Field()
    buyer = scrapy.Field()
    extend = scrapy.Field()
    product = scrapy.Field()
    risk = scrapy.Field()
    seller = scrapy.Field()
    seo = scrapy.Field()
    trade = scrapy.Field()
    transaction_list = scrapy.Field()
    transaction_countries = scrapy.Field()
    transaction_overview = scrapy.Field()
    get_time = scrapy.Field()


class ProductSupplier(scrapy.Item):
    supplier_id = scrapy.Field()
    supplier_name = scrapy.Field()
    supplier_site = scrapy.Field()
    supplier_star = scrapy.Field()
    keyword = scrapy.Field()
    post_category_id = scrapy.Field()
    product_id = scrapy.Field()
    product_image = scrapy.Field()
    product_title = scrapy.Field()
    product_url = scrapy.Field()
    product_rank_score_info = scrapy.Field()
