import json
import re
import time
from copy import deepcopy

import scrapy
from scrapy import Request
from urllib import parse as urlparse


class ProductsInShopsSpider(scrapy.Spider):
    name = 'products_in_shops'
    allowed_domains = ['alibaba.com']
    orders = []

    # start_urls = ['http://alibaba.com/']

    def start_requests(self):
        shops = ['moderndeco2015.en.alibaba.com']
        for i in shops:
            url = 'https://{0}/{1}.html'.format(i, 'productlist')
            res_item = {'site': i}
            yield Request(url=url, callback=self.parse_list, meta={'res_item': res_item}, dont_filter=True)

    def parse_list(self, response):
        res_item = response.meta['res_item']
        site = res_item['site']
        if response.status == 200:
            data_str = urlparse.unquote(
                response.xpath('//div[@module-name="icbu-pc-productListPc"]/@module-data').get())
            data = json.loads(data_str)
            product_list = data['mds']['moduleData']['data']['productList']
            if len(product_list) != 0:
                try:
                    urls = ['https://{0}{1}'.format(site, i['url']) for i in product_list]
                    yield from response.follow_all(urls=urls, callback=self.parse_page_detail,
                                                   meta={'res_item': res_item}, dont_filter=True)

                    next_page = data['mds']['moduleData']['data']['pageNavView']['currentPage'] + 1
                    next_page_format_str = data['mds']['moduleData']['data']['pageNavView']['formatString']
                    next_page_url = 'https://{0}{1}'.format(site, next_page_format_str.format(next_page))
                    yield Request(url=next_page_url, callback=self.parse_list, meta={'res_item': res_item},
                                  dont_filter=True)
                except Exception as e:
                    print('----------------')
                    print(response.request.url)
                    print(e)
                    print('----------------')
        else:
            print('网络出错')

    def parse_page_detail(self, response):
        res_item = response.meta['res_item']
        if response.status == 200:
            try:
                # 获取产品参数
                for i in response.xpath('//script').extract():
                    if len(re.findall(r'window.detailData', i)) > 0:
                        for j in i.split('\n'):
                            if len(re.findall(r'window.detailData', j)) > 0:
                                detail_data_str = j.split('window.detailData = ')[-1]
                                detail_data = json.loads(detail_data_str)

                                # 信保
                                bao_account = detail_data['globalData']['seller'][
                                    'baoAccountAmount'] if 'baoAccountAmount' in \
                                                           detail_data['globalData'][
                                                               'seller'].keys() else -1
                                # 店铺 URL
                                home_url = detail_data['globalData']['seller']['homeUrl'] if 'homeUrl' in \
                                                                                             detail_data['globalData'][
                                                                                                 'seller'].keys() else ' '

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

                                companyName = detail_data['globalData']['seller']['companyName']

                                # 获取产品首图
                                cover_url = ''
                                for im in detail_data['globalData']['product']['mediaItems']:
                                    if 'imageUrl' in im.keys():
                                        cover_url = im['imageUrl']['normal']
                                        break
                                # 管道数据

                                res_item['item_id'] = detail_data['globalData']['product']['productId']
                                res_item['subject'] = detail_data['globalData']['product']['subject']
                                res_item['product_url'] = response.request.url
                                res_item['cover_url'] = cover_url
                                res_item['keywords'] = \
                                    re.findall(r'- Buy (.+?) Product on', response.xpath('//title/text()').get())[
                                        0].split(
                                        ',')
                                res_item['bao_account'] = bao_account
                                res_item['home_url'] = home_url
                                res_item['ord_amt6m'] = ordAmt6m
                                res_item['ord_cnt6m'] = ordCnt6m
                                res_item['companyName'] = companyName
                                res_item['product_category_id']=detail_data['globalData']['product']['productCategoryId']
                                # res_item['base_properties'] = detail_data['globalData']['product']['productBasicProperties']
                                # res_item['seo'] = detail_data['globalData']['seo']

                                # print(response.request.headers)
                                # 查询订单
                                order_query_url = 'https://www.alibaba.com/' \
                                                  'event/app/productExportOrderQuery/' \
                                                  'transactionList.htm?detailId={0}&page=1'.format(
                                    detail_data['globalData']['product']['productId'])
                                yield Request(url=order_query_url,
                                              callback=self.parse_detail_order,
                                              meta={'res_item': deepcopy(res_item)},
                                              dont_filter=True
                                              )
                                # yield res_item
                        break

            except Exception as e:
                print('----------------')
                print(response.request.url)
                print(e)
                print('----------------')

        else:
            print('parse_page_detail')

    def parse_detail_order(self, response):
        res_item = response.meta['res_item']
        url = response.request.url
        res_json = json.loads(response.text)
        if response.status == 200:
            try:

                # 业务正常
                if res_json['success']:
                    # print(res_item['item_id'])
                    # print(item_id)
                    # print(url)
                    self.orders.extend(res_json['data']['orders'])
                    # 多页订单
                    if res_json['data']['totalPage'] != res_json['data']['page']:
                        order_query_url = re.sub(r'page=\d+', 'page={0}'.format(str(res_json['data']['page'] + 1)),
                                                 url)
                        # print(order_query_url)
                        # 下一页订单查询
                        # time.sleep(1)
                        yield response.follow(url=order_query_url, callback=self.parse_detail_order,
                                              meta={'res_item': deepcopy(res_item)})
                    else:
                        # 单页订单查询
                        item_id = re.findall(r'detailId=(.+?)&page', url)[0]
                        print(item_id)
                        print('单页订单查询')
                        # time.sleep(1)
                        res_item['orders'] = self.orders
                        self.orders = []
                        compare_url = 'https://www.alibaba.com/detail/compareProducts.html?ids={0}'.format(
                            res_item['item_id'])
                        yield response.follow(url=compare_url, callback=self.parse_inquires,
                                              meta={'res_item': deepcopy(res_item)})
                # 业务错误，没有订单信息
                else:
                    pass
                    ##### 略过没有订单的产品
                    # res_item['orders'] = []
                    # self.orders = []
                    # compare_url = 'https://www.alibaba.com/detail/compareProducts.html?ids={0}'.format(
                    #     res_item['item_id'])
                    # # time.sleep(1)
                    # yield response.follow(url=compare_url, callback=self.parse_inquires,
                    #                       meta={'res_item': deepcopy(res_item)})
                    ##### 略过没有订单的产品
            # yield res_item

            except Exception as e:
                print('----------------')
                print(e)
                print('----------------')
        else:
            print('订单查询网络错误')

    # 180 天类目询盘情况
    def parse_inquires(self, response):
        url = response.request.url
        res_item = response.meta['res_item']
        print(res_item['item_id'])
        print(url)

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
                                yield res_item
                                # print(json.dumps(res_item))
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
