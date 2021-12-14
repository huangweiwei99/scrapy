import json
import re
import time
from copy import deepcopy

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess


class AlibabaResultKeywordsSpider(scrapy.Spider):
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
        # print(response.request.headers['User-Agent'])
        # title = response.xpath('//title/text()').get()
        # print(title)
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
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse_result_async, dont_filter=True,
                                     meta={'offer_list': deepcopy(offerList),
                                           'keyword': deepcopy(response.meta['keyword'])})
            except Exception as e:
                print('----------------')
                print('解析详情页出错')
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
                    offer_list.extend(json_data['data']['offerList'])

                    # print(json.dumps(offer_list))
                    print('+++++++++++++++++++++++++++++++++++')
                    for i in offer_list:
                        item = {'supplierId': i['supplier']['supplierId'],
                                'supplierName': i['supplier']['supplierName'],
                                'supplierHomeHref': 'https:{0}'.format(i['supplier']['supplierHomeHref']),
                                'displayStarLevel': i['company']['displayStarLevel'],
                                'keyword': keyword,
                                'postCategoryId': i['information']['postCategoryId'],
                                'productImage': 'https:{0}'.format(i['image']['productImage']),
                                'id': i['id'],
                                'title': i['information']['puretitle'],
                                'productUrl': 'https:{0}'.format(i['information']['productUrl']),
                                'rankScoreInfo': i['information']['rankScoreInfo'],
                                }
                        yield item
                        print(json.dumps(item))

            except Exception as e:
                print('----------------')
                print('解析详情页出错')
                print(response.request.url)
                # print(detail_data_str)
                print(e)
                print('----------------')
        else:
            print('网络错误')


if __name__ == "__main__":
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
            "FEEDS": {
                "搜索结果.csv": {"format": "csv", "encoding": "utf-8", "indent": 4},
            },
            # 'PLAYWRIGHT_BROWSER_TYPE':'firefox',
        }
    )
    process.crawl(AlibabaResultKeywordsSpider)
    process.start()
