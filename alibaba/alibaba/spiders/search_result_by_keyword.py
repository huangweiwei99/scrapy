import json

import scrapy


class SearchResultByKeywordSpider(scrapy.Spider):
    name = 'search_result_by_keyword'
    allowed_domains = ['alibaba.com']
    start_urls = []

    def start_requests(self):
        url_str = 'https://open-s.alibaba.com/openservice/galleryProductOfferResultViewService?' \
                  'appName=magellan&appKey=a5m1ismomeptugvfmkkjnwwqnwyrhpb1&staticParam=&' \
                  'searchText={0}&' \
                  'IndexArea=product_en&' \
                  'asyncLoadIndex={1}&' \
                  'waterfallCtrPageId=b760dabb573e46cdbec1dbbf6deefc74&' \
                  'waterfallReqCount=1&' \
                  'page={2}&' \
                  'asyncLoad=true'

        urls = []
        for i in range(3)[1:3]:
            for j in range(102)[1:102]:
                urls.append(url_str.format('living_room_sofa', i, j))
                print(url_str.format('living_room_sofa', i, j))
        # print(urls)
        self.start_urls = urls[0:10]
        for i in self.start_urls:
            yield scrapy.Request(url=i, meta={
                'dont_redirect': True,  # 这个可以
                'handle_httpstatus_list': [301, 302]  # 这个不行
            }, callback=self.parse)

    def parse(self, response):
        json_data = json.loads(response.text)
        product_list = json_data['data']['offerList']
        # p4p
        # p4p = product_list['information']['p4p']
        for i in product_list:
            if not i['information']['p4p'] and i['reviews']['reviewCount']>0:
                print(i['information']['p4p'])
                print(i['reviews']['reviewCount'])
                print(i['id'])
                print(i['information']['productUrl'])
        # print(p4p)
        # print(json_data['data']['offerList'])
