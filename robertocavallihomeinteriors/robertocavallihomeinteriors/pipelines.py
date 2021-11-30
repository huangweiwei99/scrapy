# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import re
import time
from os.path import dirname, basename, join
from urllib.parse import urlparse

from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline

from . import settings


class RobertocavallihomeinteriorsPipeline:
    def process_item(self, item, spider):
        print('保存产品描述')
        print(item['desc'])
        desc = item['desc']
        title = item['title']
        page_url = item['page_url']
        print('++++++++++++++++')
        # txt
        with open(os.path.join(settings.FILES_STORE, title, '{0}_desc.txt'.format(title)), 'w',
                  encoding='utf-8') as f:
            f.write(desc)

        # txt
        with open(os.path.join(settings.FILES_STORE, title, '{0}_url.txt'.format(title)), 'w',
                  encoding='utf-8') as f:
            f.write(page_url)
        return item


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

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


class FileDownloadPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        media_requests = super(FileDownloadPipeline, self).get_media_requests(item, info)
        for media_request in media_requests:
            media_request.item = item
            # print('{0}的文件正在下载中.....'.format(item['title']))
        return media_requests

    def file_path(self, request, response=None, info=None):
        # 获取默认保存的文件路径
        origin_path = super(FileDownloadPipeline, self).file_path(request, response, info)
        # 过滤文件夹非法字符串
        title = re.sub(r'[\\/:\*\?"<>\|]', "", request.item['title'])
        # 修改保存文件夹路径
        save_path = origin_path.replace("full", title)
        # 重命名文件名
        for i in request.item['files']:
            if i['pdf_url'] == request.url:
                print('{0}的文件{1}正在下载中.....'.format(title, i['pdf_name']))
                return re.sub(r'\b[0-9a-f]{40}\b', i['pdf_name'] + '_' + str(int(round(time.time() * 1000))),
                              save_path)
        return origin_path
