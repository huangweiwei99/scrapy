# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os.path
import re
import time

from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class Ali1688Pipeline:
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print('get_media_requests--------------------')
        item['image_urls'] = list(map(lambda x: x['image_url'], item['images']))
        media_requests = super(ImagePipeline, self).get_media_requests(item, info)
        # print(item)
        for media_request in media_requests:
            # media_request.item['image_urls']=item
            media_request.item = item
            # print('{0}的图片正在下载中.....'.format(item['page_title']))
        # print(media_requests)
        return media_requests

    def file_path(self, request, response=None, info=None):
        origin_path = super(ImagePipeline, self).file_path(request, response, info)
        # 过滤文件夹非法字符串
        # /images/639634396102_沙发床可折叠多功能推拉收纳两用客厅小户型实木双人经济型沙发床-阿里巴巴/images
        # {sc_spid}/images/{item_id}_{title}/images
        sc_spid = request.item['sc_spid']
        item_id = request.item['item_id']
        title = re.sub(r'[\\/:\*\?"<>\|]', "", request.item['page_title'])
        save_path = origin_path.replace("full",
                                        os.path.join(sc_spid, '{0}_images'.format(sc_spid),
                                                     '{0}_{1}_{2}'.format(sc_spid, item_id, title), 'images'))
        print(save_path)
        for i in request.item['images']:
            if i['image_url'] == request.url:
                print('{0}的图片正在下载中.....'.format(request.item['page_title']))

                return re.sub(r'\b[0-9a-f]{40}\b', i['image_name'] + '_' + str(int(round(time.time() * 1000))),
                              save_path)
        return origin_path
