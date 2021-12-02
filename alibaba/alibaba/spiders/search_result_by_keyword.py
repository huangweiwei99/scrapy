import json
import re

import scrapy
from scrapy import Request


class SearchResultByKeywordSpider(scrapy.Spider):
    name = 'search_result_by_keyword'
    allowed_domains = ['alibaba.com']
    start_urls = []
    orders = []

    def start_requests(self):
        url_str = 'https://open-s.alibaba.com/openservice/galleryProductOfferResultViewService?' \
                  'appName=magellan&appKey=a5m1ismomeptugvfmkkjnwwqnwyrhpb1&staticParam=&' \
                  'searchText={0}&' \
                  'IndexArea=product_en&' \
                  'asyncLoadIndex={1}&' \
                  'waterfallCtrPageId=b760dabb573e46cdbec1dbbf6deefc74&' \
                  'waterfallReqCount=1&' \
                  'page={2}&' \
                  'asyncLoad=true'

        urls = []
        for i in range(3)[1:3]:
            for j in range(102)[1:102]:
                urls.append(url_str.format('living_room_sofa', i, j))
                # print(url_str.format('living_room_sofa', i, j))
        # print(urls)
        self.start_urls = urls[0:]
        for i in self.start_urls:
            yield scrapy.Request(url=i, meta={
                'dont_redirect': True,  # 这个可以
                'handle_httpstatus_list': [301, 302]  # 这个不行
            }, callback=self.parse_result)

    def parse_result(self, response):
        json_data = json.loads(response.text)
        product_list = json_data['data']['offerList']
        print('解析搜索结果')
        for i in product_list:
            if not i['information']['p4p'] and i['reviews']['reviewCount'] > 0:
                self.crawler.stats.inc_value('reviews_pages_crawled')
                res_item = {
                    'id': i['id'],
                    'productUrl': i['information']['productUrl'],
                    'title': i['information']['title'],
                    'puretitle': i['information']['puretitle'],
                    'productImage': i['image']['productImage'],
                    'postCategoryId': i['information']['postCategoryId'],
                    'supplierName': i['supplier']['supplierName'],
                    'supplierHomeHref': i['supplier']['supplierHomeHref'],
                    'supplierYear': i['supplier']['supplierYear'],
                    'displayStarLevel': i['company']['displayStarLevel'],
                    'transactionLevelFloat': i['company']['transactionLevelFloat'],
                    'otTotalOrdCnt': i['company']['otTotalOrdCnt'],
                    'reviews': i['reviews']['reviewCount']
                }
                order_query_url = 'https://{0}event/app/productExportOrderQuery/transactionList.htm?detailId={1}&page=1'.format(
                    i['supplier']['supplierHomeHref'], i['id'])
                # print(i['information']['productUrl'])
                yield Request(url=order_query_url,
                              meta={'res_item': res_item},
                              callback=self.parse_transaction)

    # 交易查询
    def parse_transaction(self, response):
        url = response.request.url
        res_status=response.status
        # 响应正常
        if res_status==200:
            try:
                res_item = response.meta['res_item']
                res_json = json.loads(response.text)
                compare_url = 'https://www.alibaba.com/detail/compareProducts.html?ids={0}'.format(
                    res_item['id'])
                # 业务正常
                if res_json['success']:
                    self.orders.extend(res_json['data']['orders'])
                    # 订单多页查询
                    if res_json['data']['totalPage'] != res_json['data']['page']:
                        order_query_url = re.sub(r'page=\d+', 'page={0}'.format(str(res_json['data']['page'] + 1)),
                                                 url)
                        yield Request(url=order_query_url, callback=self.parse_transaction,
                                      meta={'res_item': response.meta['res_item']})

                    # 跳出订单查询进入详情页查询
                    else:
                        # res_item = response.meta['res_item']
                        # detail_url = 'https:{0}'.format(res_item['productUrl'])
                        # print(self.orders)
                        # res_item['orders'] = self.orders
                        # yield Request(url=detail_url, callback=self.parse_detail,
                        #               meta={'res_item': res_item})
                        # self.orders = []

                        res_item['orders'] = self.orders
                        self.orders = []
                        yield Request(url=compare_url, callback=self.parse_inquires,
                                      meta={'res_item': res_item})
                # 业务异常
                else:
                    print(res_json['code'])
                    print(res_json)
                    print('跳过订单查询，进入询盘查询')
                    print('-------------------------------')
                    res_item['orders'] = []
                    self.orders = []
                    yield Request(url=compare_url, callback=self.parse_inquires,
                                  meta={'res_item': res_item})

            except Exception as e:
                print('----------------')
                print(url)
                print(e)
                print('----------------')
        # 响应异常
        else:
            print(res_status)
            print(url)
            print('交易查询网络响应异常')

    # 180 天类目询盘情况
    def parse_inquires(self, response):
        url = response.request.url

        if response.status == 200:
            res_item = response.meta['res_item']
            try:
                for i in response.xpath('//script').extract():
                    if len(re.findall(r'#J-m-compare-results', i)) > 0:
                        for j in i.split('\n'):
                            if len(re.findall('data:', j)) > 0:
                                compare_data = json.loads(j.strip().replace('data: ', ''))
                                list_view_first=compare_data['listView'][0]
                                # print(list_view_first['compareCompanyView'])
                                iquiries=list_view_first['compareCompanyView']['iquiries']
                                page_views=list_view_first['compareCompanyView']['pageViews']
                                res_item['iquiries']=iquiries
                                res_item['page_views'] = page_views
                                # print(json.dumps(res_item))
                                # print(self.crawler.stats.get_value('reviews_pages_crawled'))
                                # print(json.loads(j))
                                # 进入详情页查询
                                detail_url = 'https:{0}'.format(res_item['productUrl'])
                                yield Request(url=detail_url, callback=self.parse_detail,
                                              meta={'res_item': res_item})
                        break
            except Exception as e:
                print('----------------')
                print('180 天类目询盘情况')
                print(url)
                print(res_item['productUrl'])
                print(e)
                print('----------------')
        else:
            print(response.status)
            print('180 天类目询盘情况网络错误')

    # 详情页查询
    def parse_detail(self, response):
        if response.status == 200:
            try:
                res_item = response.meta['res_item']
                for i in response.xpath('//script').extract():
                    if len(re.findall(r'window.detailData', i)) > 0:
                        for j in i.split('\n'):
                            if len(re.findall(r'window.detailData', j)) > 0:
                                detail_data_str = j.split('window.detailData = ')[-1]
                                detail_data = json.loads(detail_data_str)

                                moq = detail_data['globalData']['product']['moq']
                                price = detail_data['globalData']['product']['price'][
                                    'formatLadderPrice'] if 'formatLadderPrice' in \
                                                            detail_data['globalData'][
                                                                'product'][
                                                                'price'].keys() else ''

                                # 关键字
                                keywords = \
                                    re.findall(r'- Buy (.+?) Product on', response.xpath('//title/text()').get())[
                                        0].split(
                                        ',')

                                # 半年GMV
                                ordAmt6m = detail_data['globalData']['seller']['tradeHalfYear'][
                                    'ordAmt6m'] if 'tradeHalfYear' in \
                                                   detail_data['globalData'][
                                                       'seller'].keys() else ' '

                                # 半年交易数
                                ordCnt6m = detail_data['globalData']['seller']['tradeHalfYear'][
                                    'ordCnt6m'] if 'tradeHalfYear' in \
                                                   detail_data['globalData'][
                                                       'seller'].keys() else ' '
                                # 信保额度
                                bao_account = detail_data['globalData']['seller'][
                                    'baoAccountAmount'] if 'baoAccountAmount' in \
                                                           detail_data['globalData'][
                                                               'seller'].keys() else -1
                                res_item['moq'] = moq
                                res_item['price'] = price
                                res_item['keywords'] = keywords
                                res_item['ordAmt6m'] = ordAmt6m
                                res_item['ordCnt6m'] = ordCnt6m
                                res_item['bao_account'] = bao_account
                                print('解析详情页')
                                print(json.dumps(res_item))
                                print(self.crawler.stats.get_value('reviews_pages_crawled'))
                                yield res_item
                                # print(response.meta['res_item'])
                                print('------------------------')
                        break
            except Exception as e:
                print('----------------')
                print('解析详情页出错')
                print(response.request.url)
                print(e)
                print('----------------')
        else:
            print('网络错误')
