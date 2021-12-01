# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import re
import time

from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline

from . import settings


class LuxurylivinggroupPipeline:
    def process_item(self, item, spider):
        print('保存产品描述')
        print(item['desc'])
        desc = item['desc']
        title = item['title']
        page_url = item['page_url']
        brand_name = item['brand_name']

        print('++++++++++++++++')
        # txt
        with open(os.path.join(settings.FILES_STORE, brand_name, title, '{0}_{1}_desc.txt'.format(brand_name, title)),
                  'w',
                  encoding='utf-8') as f:
            f.write(desc)

        # txt
        with open(os.path.join(settings.FILES_STORE, brand_name, title, '{0}_{1}_url.txt'.format(brand_name, title)),
                  'w',
                  encoding='utf-8') as f:
            f.write(page_url)
        return item


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

        media_requests = super(ImagePipeline, self).get_media_requests(item, info)
        for media_request in media_requests:
            media_request.item = item
            # print('{0}的图片正在下载中.....'.format(item['title']))
            # print(media_requests)
        return media_requests

    def file_path(self, request, response=None, info=None):
        origin_path = super(ImagePipeline, self).file_path(request, response, info)
        # 过滤文件夹非法字符串
        title = re.sub(r'[\\/:\*\?"<>\|]', "", request.item['title'])
        brand = re.sub(r'[\\/:\*\?"<>\|]', "", request.item['brand_name'])

        save_path = origin_path.replace("full", os.path.join(brand, title))
        # print(save_path)
        for i in request.item['images']:
            if i['image_url'] == request.url:
                print('{0} 品牌 {1} 的图片 {2} 正在下载中.....'.format(brand, title, i['image_name']))
                # 提取除去扩展名的文件名
                name = re.findall(r'(.+?)\.', i['image_name'])[0] + '_' + str(int(round(time.time() * 1000)))
                return re.sub(r'\b[0-9a-f]{40}\b', name, save_path)
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
        brand = re.sub(r'[\\/:\*\?"<>\|]', "", request.item['brand_name'])

        # 修改保存文件夹路径
        save_path = origin_path.replace("full", os.path.join(brand, title))
        # 重命名文件名
        for i in request.item['files']:
            if i['pdf_url'] == request.url:
                print('{0} 品牌 {1} 的文件 {2} 正在下载中.....'.format(brand, title, i['pdf_name']))
                # 提取除去扩展名的文件名
                name = re.findall(r'(.+?)\.', i['pdf_name'])[0] + '_' + str(int(round(time.time() * 1000)))
                return re.sub(r'\b[0-9a-f]{40}\b', name, save_path)
        return origin_path
