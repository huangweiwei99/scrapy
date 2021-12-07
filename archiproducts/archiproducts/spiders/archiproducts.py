import scrapy

from ..items import ImagesItem


def folder_name_filter(news_title):
    char_list = ['*', '|', ':', '?', '/', '<', '>', '"', '\\']
    news_title_result = news_title
    for i in char_list:
        if i in news_title:
            news_title_result = news_title.replace(i, "_")
    return news_title_result.strip().replace(' ', '_')


class ArchiproductSpider(scrapy.Spider):
    name = 'archiproducts'
    allowed_domains = ['archiproducts.com']
    start_urls = ['https://www.archiproducts.com/en/products/hessentia-cornelio-cappellini/fabric-sofa-gio-sofa_560054']

    def parse(self, response):
        # print(response.request.headers)
        # print(response.xpath('//title/text()').get())
        # print(response.request.url.spli t('/')[-1])

        image_titles = response.xpath(
            '//div[@class="image-container"]//img/@title').extract() if len(response.xpath(
            '//div[contains(@class,"main-carousel")]//img/@title').extract()) == 0 else response.xpath(
            '//div[contains(@class,"main-carousel")]//img/@title').extract()

        image_titles = list(map(lambda x: folder_name_filter(x), image_titles))
        title = folder_name_filter(''.join(response.xpath('//h2[@class="product-name"]//text()').extract()))
        # print(title)
        # print(image_titles)
        images2 = response.xpath(
            '//div[@class="image-container"]//img/@content').extract() if len(response.xpath(
            '//div[contains(@class,"main-carousel")]//img/@content').extract()) == 0 else response.xpath(
            '//div[contains(@class,"main-carousel")]//img/@content').extract()

        image_urls = list(map(lambda x: x.replace('-thumbs/b_', '-thumbs/2b_'), images2))

        other_images = response.xpath(
            '//div[@data-accordion-item]//figure[contains(@class,"cell")]//img/@lazy-src').extract()
        print('-----')
        # print(type(other_images))
        # print('-----')
        # print(type(image_urls))
        image_urls.extend(other_images)
        print(image_urls)
        print('-----')

        images = response.xpath(
            '//div[@class="image-container"]//img') if len(response.xpath(
            '//div[contains(@class,"main-carousel")]//img')) == 0 else response.xpath(
            '//div[contains(@class,"main-carousel")]//img')
        images = list(
            map(lambda x: {'image_url': x.xpath('./@content').get().replace('-thumbs/b_', '-thumbs/2b_'),
                           'image_name': folder_name_filter(x.xpath('./@title').get())}, images)
        )
        # print(images)
        item = ImagesItem(title=title, image_urls=[i['image_url'] for i in images], images=images)
        yield item
