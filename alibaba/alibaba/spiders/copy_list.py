import json
import re
from copy import deepcopy

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class CopyListSpider(scrapy.Spider):
    name = 'copy_list'
    allowed_domains = ['alibaba.com']
    start_urls = [
        "https://www.alibaba.com/product-detail/Single-Chairs-Fabric-Low-Price-Modern_1600405433826.html",
        "https://www.alibaba.com/product-detail/Italy-modern-style-PU-leather-armchair_60766721167.html?spm=a2700.picsearch.offer-list.6.346b5f935pVRr8"
    ]

    # sku = 'S009'

    def parse(self, response):
        if response.status == 200:
            try:
                self.crawler.stats.inc_value('cnt')
                for i in response.xpath('//script').extract():
                    if len(re.findall(r'window.detailData', i)) > 0:
                        for j in i.split('\n'):
                            if len(re.findall(r'window.detailData', j)) > 0:
                                detail_data_str = j.split('window.detailData = ')[-1]
                                detail_data = json.loads(detail_data_str)
                                # print(detail_data)
                                print(json.dumps(detail_data))
                                subject = detail_data['globalData']['product']['subject']
                                keywords = \
                                    re.findall(r'- Buy (.+?) Product on', response.xpath('//title/text()').get())[
                                        0].split(
                                        ',')
                                k1 = keywords[0]
                                for im in detail_data['globalData']['product']['mediaItems']:
                                    if 'imageUrl' in im.keys():
                                        cover_url = im['imageUrl']['normal']
                                        break
                                base_properties=detail_data['globalData']['product']['productBasicProperties']
                                feature=''
                                # for i in item['base_properties']:
                                #     if 'attrValueId' in i.keys():
                                #         sys_props.append({i['attrName']: i['attrValue']})
                                #     else:
                                #         defined_props.append({i['attrName']: i['attrValue']})
                                #         if i['attrName'] == 'Model Number':
                                #             product_model = i['attrValue']
                                # for ip in base_properties:
                                #     if 'attrValueId' in ip.keys():
                                #        if ip['attrName']=='Feature':
                                #             feature=ip['attrValue']
                                #             break
                                #     sys_props.append({ip['attrName']: ip['attrValue']})
                                # else:
                                #     defined_props.append({ip['attrName']: ip['attrValue']})
                                #     if ip['attrName'] == 'Model Number':
                                #         product_model = ip['attrValue']

                                # item['item_id'] = detail_data['globalData']['product']['productId']
                                #
                                # item['product_url'] = response.request.url
                                # item['cover_url'] = cover_url
                                # item['keywords'] = \
                                # re.findall(r'- Buy (.+?) Product on', response.xpath('//title/text()').get())[0].split(
                                #     ',')
                                # item['base_properties'] = detail_data['globalData']['product']['productBasicProperties']
                                # item['seo'] = detail_data['globalData']['seo']
                                # * 产品名称
                                # * 产品关键词
                                # 产品关键词.2
                                # 产品关键词.3
                                # * 产品图片
                                # 产品图片.2	产品图片.3	产品图片.4	产品图片.5
                                # 产品视频	详情视频	普通编辑	特点	* 是否支持邮购包装（跨境电商专用包装）	* 应用场景	* 设计风格	材质	外观风格	种类	是否可折叠	* 原产地	品牌	型号	"自定义属性
                                # * 计量单位	* 阶梯价(最小起订量).1	* 阶梯价(FOB价格).1	阶梯价(最小起订量).2	阶梯价(FOB价格).2	阶梯价(最小起订量).3	阶梯价(FOB价格).3	阶梯价(最小起订量).4	阶梯价(FOB价格).4	* 长宽高(长)	* 长宽高(宽)	* 长宽高(高)	* 毛重(KG)	* 运费模板	* 发货期(数量).1	* 发货期(预计时间).1	发货期(数量).2	发货期(预计时间).2	发货期(数量).3	发货期(预计时间).3	包装方式	包装图片	包装图片.1
                                data = {"产品名称": subject,
                                        "产品关键词": k1,
                                        "产品关键词.2": "",
                                        "产品关键词.3": "",
                                        "* 产品图片": cover_url,
                                        "产品图片.2": "",
                                        "产品图片.3": "",
                                        "产品图片.4": "",
                                        "产品图片.5": "",
                                        "产品图片.6": "",
                                        "产品视频": "",
                                        "详情视频": "",
                                        "普通编辑": "",
                                        "特点": "Adjustable (other)",
                                        "* 是否支持邮购包装（跨境电商专用包装）": "Y",
                                        "* 应用场景": "Living Room",
                                        "* 设计风格": "Contemporary",
                                        "材质": "",
                                        "外观风格": "",
                                        "种类": "",
                                        "是否可折叠": "",
                                        "外观风格": "",
                                        "种类": "",
                                        "是否可折叠": "",
                                        "* 原产地": "China",
                                        "品牌": "PLAIN HOMELAND",
                                        "型号": "S007",
                                        "自定义属性(属性名).1": "",
                                        "自定义属性(属性名).2": "",
                                        "自定义属性(属性名).3": "",
                                        "自定义属性(属性名).4": "",
                                        "自定义属性(属性名).5": "",
                                        "自定义属性(属性名).6": "",
                                        "自定义属性(属性名).7": "",
                                        "自定义属性(属性名).8": "",
                                        "自定义属性(属性名).9": "",
                                        "自定义属性(属性名).10": "",
                                        "颜色": "",
                                        "颜色(图片)": "",
                                        "尺寸": "",
                                        "可售数量": "",
                                        "价格": "",
                                        "商品编码": "",
                                        "最小起订量": "",
                                        "* 计量单位": "Piece",
                                        "* 阶梯价(最小起订量).1": 2,
                                        "* 阶梯价(FOB价格).1": 255,
                                        "阶梯价(最小起订量).2": "",
                                        "阶梯价(FOB价格).2": "",
                                        "阶梯价(最小起订量).3": "",
                                        "阶梯价(FOB价格).3": "",
                                        "阶梯价(最小起订量).4": "",
                                        "阶梯价(FOB价格).4": "",
                                        "* 长宽高(长)": "60",
                                        "* 长宽高(宽)": "70",
                                        "* 长宽高(高)": "60",
                                        "* 毛重(KG)": "150",
                                        "* 运费模板": "1",
                                        "* 发货期(数量).1": "45",
                                        "发货期(预计时间).2": "",
                                        "发货期(数量).3": "",
                                        "发货期(预计时间).3": "",
                                        "包装方式": "",
                                        "包装图片": "",
                                        "包装图片.1": ""

                                        # 阶梯价(FOB价格).1	阶梯价(最小起订量).2	阶梯价(FOB价格).2	阶梯价(最小起订量).3	阶梯价(FOB价格).3	阶梯价(最小起订量).4	阶梯价(FOB价格).4
                                        # * 长宽高(长)	* 长宽高(宽)	* 长宽高(高)	* 毛重(KG)	* 运费模板	* 发货期(数量).1	* 发货期(预计时间).1	发货期(数量).2	发货期(预计时间).2
                                        # 发货期(数量).3	发货期(预计时间).3	包装方式	包装图片	包装图片.1

                                        }
                                # aa = get_project_settings()
                                # print(aa.keys())
                                print(json.dumps(data))
                                yield data
                                # print(json.dumps(detail_data))
                                # item_id = detail_data['globalData']['product']['productId']
                                # self.crawler.stats.set_value('detail_{0}'.format(item_id), [])
                                # detail_data = detail_data['globalData']
                                # detail_data.pop('i18n', '')
                                # detail_data['sku'] = self.sku

                        break
                print('一共有 {0} 个,已经完成了 {1} 个,还有 {2} 个'.format(
                    len(self.start_urls),
                    self.crawler.stats.get_value('cnt'),
                    len(self.start_urls) - self.crawler.stats.get_value('cnt')
                )
                )
            except Exception as e:
                print('----------------')
                print('解析详情页出错')
                print(response.request.url)
                print(e)
                print('----------------')
        else:
            print('网络错误')


if __name__ == "__main__":
    process = CrawlerProcess(
        # get_project_settings()
        settings={
            "DOWNLOADER_MIDDLEWARES": {
                # 'alibaba.middlewares.AlibabaDownloaderMiddleware': 543,
                'alibaba.alibaba.middlewares.RandomUserAgentMiddleware': 1,
            },
            # 'BOT_NAME': 'alibaba',
            # "SPIDER_MODULES": ['alibaba.spiders'],
            # "NEWSPIDER_MODULE": 'alibaba.spiders',
            "ROBOTSTXT_OBEY": False,
            "LOG_LEVEL": "ERROR",
            "DOWNLOAD_DELAY": 1,
            "COOKIES_ENABLED": False,
            "AUTOTHROTTLE_ENABLED": True,
            # The initial download delay
            "AUTOTHROTTLE_START_DELAY": 1,
            # The maximum download delay to be set in case of high latencies
            "AUTOTHROTTLE_MAX_DELAY": 3,
            "FEEDS": {
                "books.csv": {"format": "csv", "encoding": "utf-8", "indent": 4},
            },

            # "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            # "DOWNLOAD_HANDLERS": {
            #     # "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            #     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            # },
        }
    )
    process.crawl(CopyListSpider)
    process.start()
