import scrapy


class DetailSpider(scrapy.Spider):
    name = 'detail'
    allowed_domains = ['alibaba.com']
    start_urls = ['https://www.alibaba.com/product-detail/Linsy-Modular-Velours-Canap-Chesterfield-Living_62413162233.html?spm=a2700.galleryofferlist.normal_offer.d_title.26504f2bjkvibe']

    def parse(self, response):
        print(response.xpath('//title/text()').get())
