import json
import re
from copy import deepcopy

import scrapy


class MoreDetailSpider(scrapy.Spider):
    name = 'more_detail'
    allowed_domains = ['alibaba.com']
    start_urls = [
        'https://www.alibaba.com/product-detail/Linsy-Modular-Velours-Canap-Chesterfield-Living_62413162233.html',
        'https://plainhomeland.en.alibaba.com/product/1600232213302-826783768/Double_Soft_Bed_New_Model_Full_King_Size_Leather_Headboard_Upholstered_Bed.html'
    ]

    def parse(self, response):
        if response.status == 200:
            try:
                for i in response.xpath('//script').extract():
                    if len(re.findall(r'window.detailData', i)) > 0:
                        for j in i.split('\n'):
                            if len(re.findall(r'window.detailData', j)) > 0:
                                detail_data_str = j.split('window.detailData = ')[-1]
                                detail_data = json.loads(detail_data_str)
                                # print(json.dumps(detail_data))
                                item_id = detail_data['globalData']['product']['productId']
                                base_url = 'https://www.en.alibaba.com/event/app/productExportOrderQuery'
                                urls = [
                                    # 订单概览
                                    '{0}/transactionOverview.htm?detailId={1}'.format(base_url, item_id),
                                    # 出口国家
                                    '{0}/transactionCountries.htm?detailId={1}'.format(base_url, item_id),
                                    # 详细订单
                                    '{0}/transactionList.htm?&size=1000&detailId={1}'.format(base_url, item_id)
                                ]
                                self.crawler.stats.set_value('detail', [])
                                detail_data = detail_data['globalData']
                                detail_data.pop('i18n', '')
                                yield from response.follow_all(urls=urls, callback=self.parse_transaction,
                                                               dont_filter=True,
                                                               meta={'detail': deepcopy(detail_data)})

                                # 获取产品首图
                                # cover_url = ''
                                # for i in detail_data['globalData']['product']['mediaItems']:
                                #     if 'imageUrl' in i.keys():
                                #         cover_url = i['imageUrl']['normal']
                                #         break
                                # cover_url = cover_url
                                # item_id = detail_data['globalData']['product']['productId']
                                # subject = detail_data['globalData']['product']['subject']
                                # product_url = response.request.url
                                # moq = detail_data['globalData']['product']['moq']
                                # price = detail_data['globalData']['product']['price']['formatLadderPrice'] if 'formatLadderPrice' in \
                                #                                                                               detail_data['globalData'][
                                #                                                                                   'product'][
                                #                                                                                   'price'].keys() else ''
                                # # 关键字
                                # keywords = re.findall(r'- Buy (.+?) Product on', response.xpath('//title/text()').get())[
                                #     0].split(
                                #     ',')
                                #
                                # companyName = detail_data['globalData']['seller']['companyName']
                                #
                                # # 半年GMV
                                # ordAmt6m = detail_data['globalData']['seller']['tradeHalfYear'][
                                #     'ordAmt6m'] if 'tradeHalfYear' in \
                                #                    detail_data['globalData'][
                                #                        'seller'].keys() else ' '
                                #
                                # # 半年交易数
                                # ordCnt6m = detail_data['globalData']['seller']['tradeHalfYear'][
                                #     'ordCnt6m'] if 'tradeHalfYear' in \
                                #                    detail_data['globalData'][
                                #                        'seller'].keys() else ' '
                                # # 信保额度
                                # bao_account = detail_data['globalData']['seller'][
                                #     'baoAccountAmount'] if 'baoAccountAmount' in \
                                #                            detail_data['globalData'][
                                #                                'seller'].keys() else -1
                                #
                                # # 产品型号
                                # sys_props = []
                                # defined_props = []
                                # product_model = ''
                                # base_properties = detail_data['globalData']['product']['productBasicProperties']
                                # for i in base_properties:
                                #     if 'attrValueId' in i.keys():
                                #         sys_props.append({'label': i['attrName'], 'value': i['attrValue']})
                                #     else:
                                #         defined_props.append({'label': i['attrName'], 'value': i['attrValue']})
                                #         if i['attrName'] == 'Model Number':
                                #             product_model = i['attrValue']
                                # print(sys_props)
                                # new_base_properties = {'sys_props': sys_props, 'defined_props': defined_props}
                                # # item = {'cover_url': cover_url, 'item_id': item_id, 'subject': subject, 'product_url': product_url,
                                # #         'moq': moq, 'base_properties': base_properties}
                                # item = {'cover_url': cover_url,
                                #         'item_id': item_id,
                                #         'subject': subject,
                                #         'keywords': keywords,
                                #         'product_url': product_url,
                                #         'moq': moq,
                                #         'price': price,
                                #         'product_model': product_model,
                                #         'base_properties': new_base_properties,
                                #         'company_name': companyName,
                                #         'ord_amt6m': ordAmt6m,
                                #         'ord_cnt6m': ordCnt6m,
                                #         'bao_account_amt': bao_account
                                #         }
                                # print(json.dumps(detail_data))
                                # yield item

                        break

            except Exception as e:
                print('----------------')
                print('解析详情页出错')
                print(response.request.url)
                print(e)
                print('----------------')
        else:
            print('网络错误')

    def parse_transaction(self, response):
        if response.status == 200:
            try:
                url = response.request.url
                item_id = url.split('=')[-1]
                meta_detail = response.meta['detail']
                if str(meta_detail['product']['productId']) == item_id:
                    # 设置初始数据
                    k_detail = self.crawler.stats.get_value('detail')
                    if 'transaction_overview' not in k_detail \
                            and 'transaction_countries' not in k_detail \
                            and 'transaction_list' not in k_detail:
                        print('start')
                        self.crawler.stats.set_value('detail', meta_detail)

                    if len(re.findall(r'transactionOverview', url)) > 0:
                        print('transactionOverview')
                        res_data = json.loads(response.text)
                        detail = self.crawler.stats.get_value('detail')
                        detail['transaction_overview'] = res_data['data'] if res_data['success'] else []
                        self.crawler.stats.set_value('detail', detail)
                        print('-------------------------------------')

                    elif len(re.findall(r'transactionCountries', url)) > 0:
                        print('transactionCountries')
                        res_data = json.loads(response.text)
                        detail = self.crawler.stats.get_value('detail')
                        detail['transaction_countries'] = res_data['data'] if res_data['success'] else []
                        self.crawler.stats.set_value('detail', detail)
                        print('-------------------------------------')

                    elif len(re.findall(r'transactionList', url)) > 0:
                        print('transactionList')
                        res_data = json.loads(response.text)
                        detail = self.crawler.stats.get_value('detail')
                        detail['transaction_list'] = res_data['data']['orders'] if res_data['success'] else []
                        self.crawler.stats.set_value('detail', detail)
                        print('-------------------------------------')

                    # 三次查询后返回结果
                    k_detail = self.crawler.stats.get_value('detail')
                    if 'transaction_overview' in k_detail \
                            and 'transaction_countries' in k_detail \
                            and 'transaction_list' in k_detail:
                        detail = self.crawler.stats.get_value('detail')
                        print(json.dumps(detail))
                        print('+++++++++++++++++++++++++++++++++++++++++++++===========================')
                        self.crawler.stats.set_value('detail', [])

            except Exception as e:
                print('----------------')
                print('解析详情页出错')
                print(response.request.url)
                print(e)
                print('----------------')
        else:
            print('网络错误')
