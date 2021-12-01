import re

import scrapy

from ..items import ProductItem


def folder_name_filter(news_title):
    char_list = ['*', '|', ':', '?', '/', '<', '>', '"', '\\']
    news_title_result = news_title
    for i in char_list:
        if i in news_title:
            news_title_result = news_title.replace(i, "_")
    return news_title_result.strip().replace(' ', '_')


class LuxurylivinggroupDetailSpider(scrapy.Spider):
    name = 'luxurylivinggroup_index'
    allowed_domains = ['luxurylivinggroup.com']
    start_urls = [
        'https://www.luxurylivinggroup.com/versace-home/',
        'https://www.luxurylivinggroup.com/fendi-casa-furniture/',
        'https://www.luxurylivinggroup.com/trussardi/',
        'https://www.luxurylivinggroup.com/bentley-home-collection/',
        'https://www.luxurylivinggroup.com/bugatti/',
        'https://www.luxurylivinggroup.com/luxury-living-outdoor/'
    ]

    def parse(self, response):
        brand_url = response.request.url
        brand_name = re.findall(r'com\/(.+?)\/', brand_url)[0]

        yield from response.follow_all(xpath='//a[@class="vc_gitem-link vc-zone-link"]',
                                       meta={'brand_url': brand_url, 'brand_name': brand_name},
                                       callback=self.parse_detail)

    def parse_detail(self, response):
        print(response.request.headers)
        print(response.xpath('//title/text()').get())

        page_url = response.request.url
        brand_name = response.meta['brand_name']
        brand_url = response.meta['brand_url']
        prod_name = response.xpath('//h1[@class="vc_custom_heading product-title"]/text()').get().replace(' ', '-')
        desc = response.xpath(
            '//div[@class="wpb_text_column wpb_content_element  product-description"]//p/text()').get()
        file_urls = response.xpath('//a[@class="qbutton default"]/@href').extract()
        files = list(map(lambda x: {'pdf_name': x.split('/')[-1], 'pdf_url': x}, file_urls))
        images = list(
            map(lambda x: {'image_name': x.split('/')[-1], 'image_url': x}, response.xpath('//li/img/@src').extract()))
        # item = {'brand_name': brand_name, 'prod_name': prod_name, 'desc': desc, 'pdf': pdf_url, 'images': images}
        # ProductItem
        # print(images)
        print(desc)
        item = ProductItem(title=prod_name,
                           images=images,
                           image_urls=[i['image_url'] for i in images],
                           files=files,
                           file_urls=file_urls,
                           desc=desc,
                           page_url=page_url,
                           brand_name=brand_name,
                           brand_url=brand_url
                           )
        yield item
