import json
import re

import scrapy


class MoreDetailSpider(scrapy.Spider):
    name = 'more_detail'
    allowed_domains = ['alibaba.com']
    start_urls = [
        'https://www.alibaba.com/product-detail/Linsy-Modular-Velours-Canap-Chesterfield-Living_62413162233.html']

    def parse(self, response):
        if response.status == 200:
            try:
                for i in response.xpath('//script').extract():
                    if len(re.findall(r'window.detailData', i)) > 0:
                        for j in i.split('\n'):
                            if len(re.findall(r'window.detailData', j)) > 0:
                                detail_data_str = j.split('window.detailData = ')[-1]
                                detail_data = json.loads(detail_data_str)
                                print(json.dumps(detail_data))
                                urls = [
                                    'https://taopinpin.en.alibaba.com/event/app/productExportOrderQuery/transactionOverview.htm?detailId=62413162233',
                                    'https://taopinpin.en.alibaba.com/event/app/productExportOrderQuery/transactionCountries.htm?detailId=62413162233'
                                ]
                                yield from response.follow_all(urls=urls, callback=self.parse_transaction,
                                                               dont_filter=True,
                                                               meta={'detail': detail_data})
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
                if len(re.findall(r'transactionOverview', url)) > 0:
                    print('transactionOverview')

                    print(json.loads(response.text))

                if len(re.findall(r'transactionCountries', url)) > 0:
                    print('transactionCountries')

                    print(json.loads(response.text))



            except Exception as e:
                print('----------------')
                print('解析详情页出错')
                print(response.request.url)
                print(e)
                print('----------------')
        else:
            print('网络错误')
