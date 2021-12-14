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
        i = "https://www.alibaba.com/products/sofa.html?IndexArea=product_en&page=2"
        yield scrapy.Request(url=i, callback=self.parse_result, dont_filter=True)

    # 搜索上半结果
    def parse_result(self, response):
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
                                     meta={'offer_list': deepcopy(offerList)})
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
                    offer_list = response.meta['offer_list']
                    res2_offer_list = json_data['data']['offerList']
                    offer_list.extend(json_data['data']['offerList'])

                    print(json.dumps(offer_list))
                    # print(res2_offer_list)
                    # products_list = dict(**res1_offer_list, **res2_offer_list)
                    # print(products_list)
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
            'DOWNLOADER_MIDDLEWARES': {
                # 'scplaywright.middlewares.ScplaywrightDownloaderMiddleware': 543,
                # 'scplaywright.middlewares.RandomUserAgentMiddleware': 543,
            },
            # 'PLAYWRIGHT_BROWSER_TYPE':'firefox',
        }
    )
    process.crawl(AlibabaResultKeywordsSpider)
    process.start()
