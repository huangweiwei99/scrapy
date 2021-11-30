import scrapy

from ..items import ProductItem


def folder_name_filter(news_title):
    char_list = ['*', '|', ':', '?', '/', '<', '>', '"', '\\']
    news_title_result = news_title
    for i in char_list:
        if i in news_title:
            news_title_result = news_title.replace(i, "_")
    return news_title_result.strip().replace(' ', '_')


class RobertocavallihomeinteriorsIndexSpider(scrapy.Spider):
    name = 'robertocavallihomeinteriors_index'
    allowed_domains = ['jumbogroup.it']
    start_urls = start_urls = ['https://robertocavallihomeinteriors.jumbogroup.it/en/products/furniture',
                               'https://robertocavallihomeinteriors.jumbogroup.it/en/products/outdoor'
                               ]

    def parse(self, response):
        yield from response.follow_all(xpath='//figure/a', callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        print(response.xpath('//title/text()').get())
        print(response.request.headers)
        page_url = response.request.url
        title = response.request.url.split('/')[-1]
        product_name = folder_name_filter(response.xpath('//h1[@class="page-intro__title"]/text()').get())
        desc = ''.join(response.xpath('//*[@id="content"]/div/div/section[2]/div/ul/li[1]/div/div//text()').extract())
        # image_urls = response.xpath('//figure/img/@src').extract()
        file_urls = response.xpath('//section[@class="section"]/div[@class="info"]//a/@href').extract()
        files = list(map(lambda x: {'pdf_name': x.split('/')[-1], 'pdf_url': x}, file_urls))
        images = list(
            map(lambda x: {'image_name': folder_name_filter(x.xpath('./@alt').get()),
                           'image_url': x.xpath('./@src').get()},
                response.xpath('//figure/img')))

        item = ProductItem(title=product_name+'_'+title,
                           images=images,
                           image_urls=[i['image_url'] for i in images],
                           files=files,
                           file_urls=file_urls,
                           desc=desc,
                           page_url=page_url
                           )
        yield item
