import html
import json
import re
import time

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ..items import ProductItem


class GetdetailSpider(scrapy.Spider):
    name = 'getdetail'

    # allowed_domains = ['dinghuovip.com']
    # start_urls = ['http://dinghuovip.com/']

    def start_requests(self):
        yield scrapy.Request(url='https://www.baidu.com', callback=self.parse, dont_filter=True)

    def parse(self, response):
        print(response.xpath('//title/text()').get())
        with open("../../bsjj.json", 'r') as load_f:
            load_dict = json.load(load_f)
            for i in load_dict[0:]:
                time.sleep(1)
                print(i['Name'])
                print(i['ModelNum'])
                # print(re.findall(r'src="(.*?)"', html.unescape(i['Description'])))

                desc_images = list(map(lambda x: {'image_name': 'D_{0}'.format(x.split('/')[-1]),
                                                  'image_url': x.replace('..', 'https://dinghuovip.com')},
                                       re.findall(r'src="(.*?)"', html.unescape(i['Description']))))
                print(desc_images)
                main_images = list(map(lambda x: {'image_name': 'M_{0}'.format(x['SaveName']),
                                                  'image_url': 'https://dinghuovip.com{0}{1}'.format(x['fileUrl'],
                                                                                                     x['SaveName'])},
                                       i['ProductImgList']))

                # main_images = [{'image_name': x.SaveName, 'image_url': 'https://dinghuovip.com{0}{1}'.format(x.fileUrl,
                #                                                                                              x.SaveName)}
                #                for x in i['ProductImgList']]
                images = desc_images + main_images
                item = ProductItem(title=i['Name'].replace(' ', '_') + '_' + i['ModelNum'],
                                   images=images,
                                   image_urls=[i['image_url'] for i in images],
                                   )
                yield item
                print(item)


# if __name__ == "__main__":
#     process = CrawlerProcess(
#         get_project_settings()
#     )
#     process.crawl(GetdetailSpider)
#     process.start()
