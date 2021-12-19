import datetime
import json
import re
import time
from copy import deepcopy

import pytz
import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess

from alibaba.alibaba.items import ProductSupplier


class AlibabaResultKeywordsSpider(scrapy.Spider):
    """
    通过关键词查找商家信息和产品信息
    """
    name = 'alibaba_result_keywords'

    def start_requests(self):
        url_str = "https://www.alibaba.com/products/{0}.html?IndexArea=product_en&page={1}"
        # urls = []
        keywords = ['living_room_sofa', 'sofa_set_furniture', 'sectional_sofa', 'sectional_couch', 'modular_sofa',
                    'sofa', 'the_sofa', ]
        # keywords = ['living_room_sofa']
        for k in keywords:
            for j in range(102)[1:102]:
                url = url_str.format(k, j)
                print(url)
                time.sleep(1)
                yield scrapy.Request(url=url, callback=self.parse_result, dont_filter=True,
                                     meta={'keyword': deepcopy(k)})

    # 搜索上半结果
    def parse_result(self, response):
        if response.status == 200:
            try:
                for i in response.xpath('//script').extract():
                    if len(re.findall(r'window.__page__data__config ', i)) > 0:
                        for j in i.split('\n'):
                            if len(re.findall(r'window.__page__data__config = ', j)) > 0:
                                json_data_str = j.split('window.__page__data__config = ')[-1]
                                json_data = json.loads(json_data_str)
                                break
                # 上半页结果
                offerList = json_data['props']['offerResultData']['offerList']
                asyncRequestUrl = json_data['props']['offerResultData']['asyncRequestUrl']
                url = 'https://open-s.alibaba.com/openservice/galleryProductOfferResultViewService?' \
                      'appName=magellan&appKey=a5m1ismomeptugvfmkkjnwwqnwyrhpb1{0}'.format(
                    asyncRequestUrl)
                yield scrapy.Request(url=url, callback=self.parse_result_async, dont_filter=True,
                                     meta={'offer_list': deepcopy(offerList),
                                           'keyword': deepcopy(response.meta['keyword'])})
            except Exception as e:
                print('----------------')
                print('解析详情页出错')
                print('上半部分，关键词：{0}'.format(response.meta['keyword']))
                print(response.request.url)
                # print(detail_data_str)
                print(e)
                print('----------------')
        else:
            print('网络错误')
        self.crawler.stats.inc_value('pc_url')

    # 搜索下半结果
    def parse_result_async(self, response):
        if response.status == 200:
            try:
                json_data = json.loads(response.text)
                # print(json_data['code'] == 200)
                # flag=json_data['code'] == 200
                if json_data['code'] == 200:
                    keyword = response.meta['keyword']
                    offer_list = response.meta['offer_list']
                    if 'offerList' in json_data['data'].keys():
                        offer_list.extend(json_data['data']['offerList'])

                    # print(json.dumps(offer_list))
                    print('+' * 100)
                    for i in offer_list:
                        item = {'supplier_id': i['supplier']['supplierId'],
                                'supplier_name': i['supplier']['supplierName'],
                                'supplier_site': 'https:{0}'.format(i['supplier']['supplierHomeHref']),
                                'supplier_star': i['company']['displayStarLevel'],
                                'keyword': keyword,
                                'post_category_id': i['information']['postCategoryId'],
                                'product_image': 'https:{0}'.format(i['image']['productImage']),
                                'product_id': i['id'],
                                'product_title': i['information']['puretitle'],
                                'product_url': 'https:{0}'.format(i['information']['productUrl']),
                                'product_rank_score_info': i['information']['rankScoreInfo'],
                                }
                        yield item
                        print(json.dumps(item))
                        # yield ProductSupplier(
                        #     supplier_id=item['supplier_id'],
                        #     supplier_name=item['supplier_name'],
                        #     supplier_site=item['supplier_site'],
                        #     supplier_star=item['supplier_star'],
                        #     keyword=item['keyword'],
                        #     post_category_id=item['post_category_id'],
                        #     product_id=item['product_id'],
                        #     product_image=item['product_image'],
                        #     product_title=item['product_title'],
                        #     product_url=item['product_url'],
                        #     product_rank_score_info=item['product_rank_score_info'],
                        # )

            except Exception as e:
                print('----------------')
                print('解析详情页出错')
                print('下半部分，关键词：{0}'.format(response.meta['keyword']))
                print(response.request.url)
                print(e)
                print('----------------')
        else:
            print('网络错误')


if __name__ == "__main__":
    today = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d_%H-%M-%S")
    process = CrawlerProcess(
        settings={
            # "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            # "DOWNLOAD_HANDLERS": {
            #     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            #     # "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            # },
            'AUTOTHROTTLE_ENABLED': True,
            'AUTOTHROTTLE_START_DELAY': 1,
            'AUTOTHROTTLE_MAX_DELAY': 3,
            'DOWNLOADER_MIDDLEWARES': {
                'alibaba.alibaba.middlewares.RandomUserAgentMiddleware': 1,
                # 'scplaywright.middlewares.ScplaywrightDownloaderMiddleware': 543,
                # 'scplaywright.middlewares.RandomUserAgentMiddleware': 543,
            },
            'ITEM_PIPELINES': {
                # 'alibaba.pipelines.AlibabaPipeline': 300,
                'alibaba.alibaba.pipelines.SearchResultMongoPipeline': 300,
            },
            'MONGO_URI': 'mongodb://skydot.f3322.net:49186',
            'MONGO_DB': "alibaba",
            'MONGO_USER': "admin",
            'MONGO_PSW': "123456",
            "FEEDS": {
                "搜索结果_{0}.csv".format(today): {"format": "csv", "encoding": "utf-8", "indent": 4},
            },
            # 'PLAYWRIGHT_BROWSER_TYPE':'firefox',
        }
    )
    process.crawl(AlibabaResultKeywordsSpider)
    process.start()
