import scrapy

from ..items import PachanItem


class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['www.pachan.com.cn']
    start_urls = [
        'http://www.pachan.com.cn/products.aspx?type=4',
        'http://www.pachan.com.cn/products.aspx?type=5',
        'http://www.pachan.com.cn/products.aspx?type=6',
        'http://www.pachan.com.cn/products.aspx?type=7',
        'http://www.pachan.com.cn/products.aspx?type=8',
        'http://www.pachan.com.cn/products.aspx?type=9',
        'http://www.pachan.com.cn/products.aspx?type=11',
        'http://www.pachan.com.cn/products.aspx?type=12',
        'http://www.pachan.com.cn/products.aspx?type=13',
        'http://www.pachan.com.cn/products.aspx?type=14',
        'http://www.pachan.com.cn/products.aspx?type=10',
        'http://www.pachan.com.cn/products.aspx?type=15',
        'http://www.pachan.com.cn/products.aspx?type=16',
        'http://www.pachan.com.cn/products.aspx?type=17',
        'http://www.pachan.com.cn/products.aspx?type=18'
                  ]

    def parse(self, response):
        print(response.xpath('//title/text()').get())
        # box=response.xpath('//div[@class="box"]')
        for i in response.xpath('//div[@class="box"]'):
            series = i.xpath('.//h3/text()').get()
            title = i.xpath('.//p/text()').get()
            image_url = 'http://www.pachan.com.cn/{0}'.format(i.xpath('.//img/@src').get())
            item = PachanItem(series=series, title=title, images=[{'image_name': title, 'image_url': image_url}])
            yield item
        yield from response.follow_all(xpath='//*[@id="PageControl"]/a', callback=self.parse)
