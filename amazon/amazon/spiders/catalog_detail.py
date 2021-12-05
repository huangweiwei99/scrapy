import re

import scrapy


class DetailSpider(scrapy.Spider):
    name = 'catalog_detail'
    allowed_domains = ['amazon.com']
    start_urls = [
        # 'https://www.amazon.com/Shintenchi-Convertible-Sectional-Reversible-Apartment/dp/B08GX586TD/ref=zg_bs_3733551_2?_encoding=UTF8&psc=1&refRID=10QM1BPANY2ZV3J1WKFG',
        # 'https://www.amazon.com/Serta-RNE-3S-BK-SET-Collection-Convertible-L66-1/dp/B07KD63YQF/ref=zg_bs_3733551_1?_encoding=UTF8&refRID=ZKZ156AX8G9X848Q75QT&th=1'
        'https://www.amazon.com/Best-Choice-Products-Leather-Recliner/dp/B01LXDH29Y?th=1',
        'https://www.amazon.com/Solutions-KD-Rolled-Arm-Collection-Micro-Fabric/dp/B07KQ5FZ7Z?th=1'
    ]

    def parse(self, response):
        print(response.request.headers)
        print(response.status)
        print(response.xpath('//title/text()').get())
        # product_name = response.xpath('//*[@id="productTitle"]/text()').get().strip()
        # brand = response.xpath('//tr[@class="a-spacing-small"][7]/td[2]//text()').extract()
        # view = response.xpath('//*[@id="acrCustomerReviewText"]/text()').get()
        # view_cnt = re.sub(r'\D', '', view)
        # item = {'product_name': product_name, 'brand': brand, 'view_cnt': view_cnt}
        # print(item)
