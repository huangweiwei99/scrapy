import json
import re
import time

import scrapy

from urllib import parse as urlparse

from scrapy import Request


class BestSellFromShopSpider(scrapy.Spider):
    name = 'best_sell_from_shop'
    allowed_domains = ['alibaba.com']
    start_urls = []
    orders = []

    def start_requests(self):
        shops = [
            # 'richfurniture001.en.alibaba.com'
            # 'linsyhome.en.alibaba.com'
            'moderndeco2015.en.alibaba.com'
            # '//fitathome.en.alibaba.com/', '//enmorning.en.alibaba.com/',
            # '//jieqifactory.en.alibaba.com/',
            # '//boomingmaxes.en.alibaba.com/', '//zuofan1.en.alibaba.com/'
        ]
        # urls = ['https:{0}productlist.html'.format(i) for i in shops]
        for i in shops:
            # url = 'https://{0}/featureproductlist.html'.format(i)
            url = 'https://{0}/productlist.html'.format(i)
            res_item = {'site': i}
            yield scrapy.Request(url=url, meta={
                'dont_redirect': True,  # 这个可以
                'handle_httpstatus_list': [301, 302],  # 这个不行
                'res_item': res_item
            }, callback=self.parse_productlist)

    def parse_productlist(self, response):
        res_status = response.status
        url = response.request.url
        print('产品列表')
        # print(response.xpath('//title/text()').get())

        res_item = response.meta['res_item']
        site = res_item['site']
        if response.status == 200:
            try:
                data_str = urlparse.unquote(
                    response.xpath('//div[@module-name="icbu-pc-productListPc"]/@module-data').get())
                data = json.loads(data_str)
                product_list = data['mds']['moduleData']['data']['productList']
                if len(product_list) != 0:
                    # urls = ['https://{0}{1}'.format(site, i['url']) for i in product_list]
                    # yield from response.follow_all(urls=urls,
                    #                                callback=self.parse_detail_page,
                    #                                meta={'res_item': res_item})

                    for i in product_list:
                        # print(i)
                        url = 'https://{0}{1}'.format(site, i['url'])
                        # print(url),
                        yield Request(url=url, callback=self.parse_detail_page, meta={'res_item': res_item},
                                      dont_filter=True)

                    next_page = data['mds']['moduleData']['data']['pageNavView']['currentPage'] + 1
                    next_page_format_str = data['mds']['moduleData']['data']['pageNavView']['formatString']
                    next_page_url = 'https://{0}{1}'.format(site, next_page_format_str.format(next_page))
                    yield Request(url=next_page_url,
                                  callback=self.parse_productlist,
                                  meta={'res_item': res_item},
                                  # dont_filter=True
                                  )

                # if len(product_list) == 0:
                #     for i in product_list:
                #         # print(i)
                #         url = 'https://{0}{1}'.format(site, i['url'])
                #         print(url)
                #         # yield Request(url=url, callback=self.parse_detail)
                # else:
                #     next_page = data['mds']['moduleData']['data']['pageNavView']['currentPage'] + 1
                #     next_page_format_str = data['mds']['moduleData']['data']['pageNavView']['formatString']
                #     next_page_url = 'https:{0}{1}'.format(site, next_page_format_str.format(next_page))
                #     print(next_page_url)
                #     yield Request(url=next_page_url, callback=self.parse_productlist, meta={'site': site})

            except Exception as e:
                print('----------------')
                print(e)
                # print(response.text)
                print('----------------')

        else:
            print(res_status)
            print(url)
            print('网络响应异常')

    # 详情页查询
    def parse_detail_page(self, response):
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
                                # 获取产品首图
                                cover_url = ''
                                for im in detail_data['globalData']['product']['mediaItems']:
                                    if 'imageUrl' in im.keys():
                                        cover_url = im['imageUrl']['normal']
                                        break

                                res_item['moq'] = moq
                                res_item['price'] = price
                                res_item['keywords'] = keywords
                                res_item['ordAmt6m'] = ordAmt6m
                                res_item['ordCnt6m'] = ordCnt6m
                                res_item['bao_account'] = bao_account
                                res_item['item_id'] = detail_data['globalData']['product']['productId']
                                res_item['subject'] = detail_data['globalData']['product']['subject']
                                res_item['product_url'] = response.request.url
                                res_item['cover_url'] = cover_url
                                res_item['keywords'] = \
                                    re.findall(r'- Buy (.+?) Product on', response.xpath('//title/text()').get())[
                                        0].split(
                                        ',')
                                print('解析详情页')
                                # print(json.dumps(res_item))
                                # print(self.crawler.stats.get_value('reviews_pages_crawled'))
                                # yield res_item
                                # print(response.meta['res_item'])
                                print('------------------------')
                                order_query_url = 'https://{0}/event/app/productExportOrderQuery/' \
                                                  'transactionList.htm?detailId={1}&page=1'.format(
                                    res_item['site'], detail_data['globalData']['product']['productId'])
                                print(detail_data['globalData']['product']['productId'])
                                yield Request(url=order_query_url,
                                              meta={'res_item': res_item},
                                              callback=self.parse_transaction,
                                              dont_filter=True

                                              )
                        break
            except Exception as e:
                print('----------------')
                print('解析详情页出错')
                print(response.request.url)
                print(e)
                print('----------------')
        else:
            print('网络错误')

    # 交易查询
    def parse_transaction(self, response):
        url = response.request.url
        print(url)
        res_status = response.status
        res_item = response.meta['res_item']
        res_json = json.loads(response.text)
        yield res_item
        # # 响应正常
        # if res_status == 200:
        #     try:
        #         # 业务正常
        #         if res_json['success']:
        #
        #             # 订单多页查询
        #             if res_json['data']['totalPage'] != res_json['data']['page']:
        #                 order_query_url = re.sub(r'page=\d+', 'page={0}'.format(str(res_json['data']['page'] + 1)),
        #                                          url)
        #                 time.sleep(2)
        #                 self.orders.extend(res_json['data']['orders'])
        #                 print(order_query_url)
        #                 yield Request(url=order_query_url, callback=self.parse_transaction,
        #                               meta={'res_item': response.meta['res_item']},
        #                               # dont_filter=True
        #                               )
        #
        #             # 跳出订单查询进入详情页查询
        #             else:
        #                 print('订单数量:{0}'.format(len(self.orders)))
        #                 res_item['orders'] = self.orders
        #                 # print(res_item)
        #                 self.orders = []
        #                 compare_url = 'https://www.alibaba.com/detail/compareProducts.html?ids={0}'.format(
        #                     res_item['item_id'])
        #                 print(res_item['item_id'])
        #                 # print(compare_url)
        #                 # yield Request(url=compare_url, callback=self.parse_inquires,
        #                 #               meta={'res_item': res_item},
        #                 #               # dont_filter=True
        #                 #               )
        #
        #                 yield res_item
        #
        #                 # res_item = response.meta['res_item']
        #                 # detail_url = 'https:{0}'.format(res_item['productUrl'])
        #                 # print(self.orders)
        #                 # res_item['orders'] = self.orders
        #                 # yield Request(url=detail_url, callback=self.parse_detail,
        #                 #               meta={'res_item': res_item})
        #                 # self.orders = []
        #         # 业务异常
        #         else:
        #             # print(res_json['code'])
        #             # print(res_json)
        #             print(str(res_json['code']) + '不存在订单: 跳过订单查询，进入询盘查询')
        #             print('-------------------------------')
        #             # res_item['orders'] = []
        #             res_item['orders'] = []
        #             self.orders = []
        #             compare_url = 'https://www.alibaba.com/detail/compareProducts.html?ids={0}'.format(
        #                 res_item['item_id'])
        #             yield Request(url=compare_url, callback=self.parse_inquires,
        #                           meta={'res_item': res_item},
        #                           # dont_filter=True
        #                           )
        #
        #     except Exception as e:
        #         print('----------------')
        #         print(url)
        #         print(e)
        #         print('----------------')
        # # 响应异常
        # else:
        #     print(res_status)
        #     print(url)
        #     self.orders = []
        #     print('交易查询网络响应异常')

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
                                list_view_first = compare_data['listView'][0]
                                # print(list_view_first['compareCompanyView'])
                                iquiries = list_view_first['compareCompanyView']['iquiries']
                                page_views = list_view_first['compareCompanyView']['pageViews']
                                res_item['iquiries'] = iquiries
                                res_item['page_views'] = page_views
                                # print(json.dumps(res_item))
                                yield res_item
                                # print(self.crawler.stats.get_value('reviews_pages_crawled'))
                                # print(json.loads(j))
                                # 进入详情页查询
                                # detail_url = 'https:{0}'.format(res_item['productUrl'])
                                # yield Request(url=detail_url, callback=self.parse_detail,
                                #               meta={'res_item': res_item})
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
