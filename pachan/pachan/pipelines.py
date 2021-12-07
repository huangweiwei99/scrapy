# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import re
import time

from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class PachanPipeline:
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        item['image_urls'] = list(map(lambda x: x['image_url'], item['images']))
        media_requests = super(ImagePipeline, self).get_media_requests(item, info)
        for media_request in media_requests:
            media_request.item = item
            print('{0}的图片正在下载中.....'.format(item['title']))
            # print(media_requests)
        return media_requests

    def file_path(self, request, response=None, info=None):
        origin_path = super(ImagePipeline, self).file_path(request, response, info)
        # 过滤文件夹非法字符串
        timestamp = str(int(round(time.time() * 1000)))
        title = re.sub(r'[\\/:\*\?"<>\|]', "", request.item['title'])
        series = re.sub(r'[\\/:\*\?"<>\|]', "", request.item['series'])

        save_path = origin_path.replace("full", os.path.join(series, title + '_' + timestamp))
        for i in request.item['images']:
            if i['image_url'] == request.url:
                print('{0} 品牌 {1} 的图片 {2} 正在下载中.....'.format(series, title, i['image_name']))
                # 提取除去扩展名的文件名
                name = series+'_'+title + '_' + timestamp
                return re.sub(r'\b[0-9a-f]{40}\b', name, save_path)
        return save_path
