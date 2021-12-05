import glob
import json
import os
import re
from copy import deepcopy

import scrapy

from .. import settings
from ..items import DetailItem


# 获取当前目录下所有的文件夹名字
# > https://www.cnblogs.com/TTyb/p/6524465.html
def getfilename(filename):
    for root, dirs, files in os.walk(filename):
        array = dirs
        if array:
            return array


class HtmlDetailSpider(scrapy.Spider):
    name = 'html_detail'
    allowed_domains = ['alibaba.com', 'tmall.com']
    arr = []

    # sc_spid = '1600083400496'

    # start_urls = [
    #     'file:///Volumes/download/工作/运营/博领/采集/国际站/TOP50排行榜/客厅家具/1600083400496/1600083400496_html/沙发床可折叠多功能推拉收纳两用客厅小户型实木双人经济型沙发床-阿里巴巴.html']

    def start_requests(self):

        # IMAGES_STORE
        # print(settings.IMAGES_STORE)
        # print('asdadasdad')
        # print(getfilename(settings.IMAGES_STORE))
        for i in getfilename(settings.IMAGES_STORE):
            item_id_path = os.path.join(settings.IMAGES_STORE, i)
            if getfilename(item_id_path) is not None:
                if '{0}_html'.format(i) in getfilename(item_id_path):
                    # print(item_id_path)
                    print('{0}_html'.format(i))
                    file_path = os.path.join(item_id_path, '{0}_html'.format(i))
                    # print(file_path)
                    # path_dir = r'Z:\工作\运营\博领\html\S021/*.html'
                    path_dir = os.path.join(file_path, '*.html')
                    html_paths = glob.iglob(path_dir)
                    for f in html_paths:
                        url = 'file://{0}'.format(f)
                        res_item = {'sc_spid': i}
                        yield scrapy.Request(url=url,
                                             callback=self.parse,
                                             meta={'res_item': deepcopy(res_item)},
                                             dont_filter=True)
                        # print('file://{0}'.format(f))

    def parse(self, response):
        # print(response.xpath('//meta[@name="b2c_auction"]/@content').get())
        # title = response.xpath('//title/text()').get()
        # print(title)
        # pass
        self.crawler.stats.inc_value('now_cnt')
        sc_spid = response.meta['res_item']['sc_spid']
        # 页面标题
        title = response.xpath('//title/text()').get()
        item_id = response.xpath('//meta[@name="b2c_auction"]/@content').get()
        # 页面链接
        href = response.xpath('//meta[@name="savepage-url"]/@content').get()
        # 缩略图 json
        for i in response.xpath('//script').extract():
            if len(re.findall(r'skuProps:', i)) > 0:
                for j in i.split('\n'):
                    if len(re.findall(r'skuProps:', j)) > 0:
                        sku_props_str = j.split('skuProps:')[-1].replace('],', ']')
                        sku_props = json.loads(sku_props_str)
                        # print(sku_props)
                break

        detail_url = response.xpath('//div[@id="desc-lazyload-container"]/@data-tfs-url').get()
        item = {'sc_spid': sc_spid, 'item_id': item_id, 'title': title, 'sku_props': sku_props,
                'detail_url': detail_url, 'page_url': href}
        # print(item)
        # print(response.request.headers)
        # print(detail_url)
        # 请求详情页
        yield scrapy.Request(url=detail_url,
                             callback=self.parse_detail_url,
                             meta={'res_item': deepcopy(item)},
                             dont_filter=True)

    def parse_detail_url(self, response):
        # print(response.request.headers)

        # print(response.text)
        # print(res_item)

        # links_cnt = self.crawler.stats.get_value('now_cnt')

        res_item = response.meta['res_item']

        # 提取详情页图片
        d_imgs_arr = re.findall(r'https?://[^>]*\.jpg', response.text)
        res_item['d_images'] = d_imgs_arr
        # print(json.dumps(res_item))
        images = list(
            map(lambda x: {'image_name': 'D{0}'.format(res_item['d_images'].index(x)),
                           'image_url': x}, res_item['d_images'])
        )
        # m_images=list(map(lambda x:{'image_name': 1,'image_url':3}))

        for i in res_item['sku_props']:
            for j in i['value']:
                if 'imageUrl' in j.keys():
                    images.append(
                        {'image_name': 'M{0}_{1}'.format(i['value'].index(j), j['name']),
                         'image_url': j['imageUrl']
                         }
                    )

        item = DetailItem(
            item_id=res_item['item_id'],
            page_title=res_item['title'],
            page_url=res_item['page_url'],
            sku_props=res_item['sku_props'],
            images=images,
            sc_spid=res_item['sc_spid']

            # detail_images=res_item['d_images'],
        )
        yield item
        print('一共{0}个产品链接, 已经完成{1}个, 还有{2}个'.format(len(self.start_urls),
                                                    self.crawler.stats.get_value('now_cnt'),
                                                    len(self.start_urls) - self.crawler.stats.get_value('now_cnt')))
        print('========================================================================')
