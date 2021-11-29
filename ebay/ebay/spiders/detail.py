import scrapy


class DetailSpider(scrapy.Spider):
    name = 'detail'
    allowed_domains = ['ebay.com']
    start_urls = ['https://www.ebay.com/itm/373455222117?hash=item56f3aa7565%3Ag%3Aws0AAOSwWXVhN5v-&LH_BIN=1&LH_ItemCondition=1000']

    def parse(self, response):
        print(response.xpath('//title/text()').get())
