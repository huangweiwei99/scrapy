import scrapy

from ..items import ProductItem


def folder_name_filter(news_title):
    char_list = ['*', '|', ':', '?', '/', '<', '>', '"', '\\']
    news_title_result = news_title
    for i in char_list:
        if i in news_title:
            news_title_result = news_title.replace(i, "_")
    return news_title_result.strip().replace(' ', '_')


class RobertocavallihomeinteriorsDetailSpider(scrapy.Spider):
    name = 'robertocavallihomeinteriors_detail'
    allowed_domains = ['jumbogroup.it']
    start_urls = ['https://robertocavallihomeinteriors.jumbogroup.it/en/products/furniture/sofas/blake']

    # def start_requests(self):
    #     for i in self.start_urls:
    #         yield scrapy.Request(url=i, meta={
    #             'dont_redirect': True,  # 这个可以
    #             'handle_httpstatus_list': [301, 302]  # 这个不行
    #         }, callback=self.parse)

    def parse(self, response):
        print(response.xpath('//title/text()').get())
        print(response.request.headers)
        page_url = response.request.url
        title = response.request.url.split('/')[-1]
        # product_name = folder_name_filter(response.xpath('//h1[@class="page-intro__title"]/text()').get())
        desc = ''.join(response.xpath('//*[@id="content"]/div/div/section[2]/div/ul/li[1]/div/div//text()').extract())
        # image_urls = response.xpath('//figure/img/@src').extract()
        file_urls = response.xpath('//section[@class="section"]/div[@class="info"]//a/@href').extract()
        files = list(map(lambda x: {'pdf_name': x.split('/')[-1], 'pdf_url': x}, file_urls))
        images = list(
            map(lambda x: {'image_name': folder_name_filter(x.xpath('./@alt').get()),
                           'image_url': x.xpath('./@src').get()},
                response.xpath('//figure/img')))

        item = ProductItem(title=title,
                           images=images,
                           image_urls=[i['image_url'] for i in images],
                           files=files,
                           file_urls=file_urls,
                           desc=desc,
                           page_url=page_url
                           )
        yield item
