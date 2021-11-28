# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import time
from os.path import join, basename, dirname
from urllib.parse import urlparse

from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline

from scrapy.pipelines.images import ImagesPipeline

from . import settings


class ArchiproductsPipeline:
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

        print('--------------------')
        media_requests = super(ImagePipeline, self).get_media_requests(item, info)
        for media_request in media_requests:
            media_request.item = item
            print('{0}的图片正在下载中.....'.format(item['title']))
            # print(media_requests)
        return media_requests

    def file_path(self, request, response=None, info=None):
        origin_path = super(ImagePipeline, self).file_path(request, response, info)
        # 过滤文件夹非法字符串
        title = re.sub(r'[\\/:\*\?"<>\|]', "", request.item['title'])
        save_path = origin_path.replace("full", title)
        for i in request.item['images']:
            if i['image_url'] == request.url:
                return re.sub(r'\b[0-9a-f]{40}\b', i['image_name'] + '_' + str(int(round(time.time() * 1000))),
                              save_path)
        return save_path

