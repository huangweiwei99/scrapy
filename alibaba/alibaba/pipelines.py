# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
import re

import pymongo
from itemadapter import ItemAdapter
# from scrapy import crawler
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings


class AlibabaPipeline:
    def process_item(self, item, spider):
        return item


class DetailMongoPipeline(object):
    collection = 'product_details'

    def __init__(self, mongo_uri, mongo_db, mongo_user, mongo_pwd):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        # self.mongo_user = mongo_user
        # self.mongo_pwd = mongo_pwd

        self.client = pymongo.MongoClient(self.mongo_uri, username='admin', password=mongo_pwd)
        self.db = self.client[self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        """
        scrapy为我们访问settings提供了这样的一个方法，这里，
        我们需要从settings.py文件中，取得数据库的URI和数据库名称
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_user=crawler.settings.get('MONGO_USER'),
            mongo_pwd=crawler.settings.get('MONGO_PSW'),
        )

    def open_spider(self, spider):
        """
        爬虫一旦开启，就会实现这个方法，连接到数据库
        """
        # self.db.authenticate(self.mongo_user, self.mongo_pwd)

    def close_spider(self, spider):
        """
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        """
        # if not item['title']:
        #     return item

        data = {
            'abtest': item['abtest'],
            'buyer': item['buyer'],
            'extend': item['extend'],
            'product': item['product'],
            'risk': item['risk'],
            'seller': item['seller'],
            'seo': item['seo'],
            'trade': item['trade'],
            'transaction_list': item['transaction_list'],
            'transaction_countries': item['transaction_countries'],
            'transaction_overview': item['transaction_overview'],
            'get_time': datetime.timestamp(datetime.now()),
        }
        table = self.db[self.collection]
        table.insert_one(data)
        return item
