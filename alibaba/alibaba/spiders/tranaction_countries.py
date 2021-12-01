import json

import scrapy


class TranactionCountriesSpider(scrapy.Spider):
    name = 'tranaction_countries'
    allowed_domains = ['alibaba.com']
    start_urls = []
    base_url = 'https://taopinpin.en.alibaba.com/event/app/productExportOrderQuery/transactionCountries.htm?detailId={0}'

    def start_requests(self):
        ids=['1600145084062']
        self.start_urls=[self.base_url.format(i) for i in ids]
        for i in self.start_urls:
            yield scrapy.Request(url=i, meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [301, 302]
            }, callback=self.parse)

    def parse(self, response):
        if response.status==200:
            try:
                data=json.loads(response.text)
                print(json.dumps(data))
            except Exception as e:
                print('----------------')
                print('解析页面出错')
                print(response.request.url)
                print(e)
                print('----------------')
        else:
            print('网路出错')
