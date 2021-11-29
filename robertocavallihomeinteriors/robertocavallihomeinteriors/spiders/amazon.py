import re

import scrapy


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/Serta-RNE-3S-BK-SET-Collection-Convertible-L66-1/dp/B07KD63YQF/ref=zg_bs_3733551_1?_encoding=UTF8&refRID=ZKZ156AX8G9X848Q75QT&th=1']

    def parse(self, response):
        print(response.xpath('//*[@id="productTitle"]/text()').get().strip())
        print(response.xpath('//tr[@class="a-spacing-small"][7]/td[2]//text()').extract())
        fb = response.xpath('//*[@id="acrCustomerReviewText"]/text()').get()
        print(re.sub(r'\D', '', fb))
