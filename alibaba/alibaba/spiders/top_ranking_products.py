import scrapy

chair=[{"title":"Living Room Chair","href":"https://sale.alibaba.com/p/exhibition/dippueokr/index.html?spm=a27aq.25248930.4539339250.21.7eae54d7EEV7Uk&wx_screen_direc=portrait&wx_navbar_transparent=true&path=/p/exhibition/dippueokr/index.html&ncms_spm=a27aq.25248930&prefetchKey=exhibition&cardType=101001652&cardId=103000002321097&topOfferIds=1600236774254&templateBusinessCode=2021-11-01-jiajuyuanyizhanhui"},{"title":"Synthetic Leather Dining Chairs","href":"https://sale.alibaba.com/p/exhibition/dippueokr/index.html?spm=a27aq.25248930.4539339250.22.7eae54d7EEV7Uk&wx_screen_direc=portrait&wx_navbar_transparent=true&path=/p/exhibition/dippueokr/index.html&ncms_spm=a27aq.25248930&prefetchKey=exhibition&cardType=101001652&cardId=103000010684596&topOfferIds=62007922432&templateBusinessCode=2021-11-01-jiajuyuanyizhanhui"},{"title":"Fabric Living Room Chairs","href":"https://sale.alibaba.com/p/exhibition/dippueokr/index.html?spm=a27aq.25248930.4539339250.23.7eae54d7EEV7Uk&wx_screen_direc=portrait&wx_navbar_transparent=true&path=/p/exhibition/dippueokr/index.html&ncms_spm=a27aq.25248930&prefetchKey=exhibition&cardType=101001652&cardId=103000008047996&topOfferIds=1600199575147&templateBusinessCode=2021-11-01-jiajuyuanyizhanhui"},{"title":"Stainless Steel Sofa Chair","href":"https://sale.alibaba.com/p/exhibition/dippueokr/index.html?spm=a27aq.25248930.4539339250.24.7eae54d7EEV7Uk&wx_screen_direc=portrait&wx_navbar_transparent=true&path=/p/exhibition/dippueokr/index.html&ncms_spm=a27aq.25248930&prefetchKey=exhibition&cardType=101001652&cardId=103000045703032&topOfferIds=62328953167&templateBusinessCode=2021-11-01-jiajuyuanyizhanhui"},{"title":"Modern Sofa Chair","href":"https://sale.alibaba.com/p/exhibition/dippueokr/index.html?spm=a27aq.25248930.4539339250.25.7eae54d7EEV7Uk&wx_screen_direc=portrait&wx_navbar_transparent=true&path=/p/exhibition/dippueokr/index.html&ncms_spm=a27aq.25248930&prefetchKey=exhibition&cardType=101001652&cardId=103000032608784&topOfferIds=1600342343504&templateBusinessCode=2021-11-01-jiajuyuanyizhanhui"}]


class TopRankingProductsSpider(scrapy.Spider):
    name = 'top-ranking-products'
    allowed_domains = ['alibaba.com']
    start_urls = ['https://sale.alibaba.com/p/exhibition/dippueokr/index.html?spm=a27aq.25248930.4539339250.23.78aa4b26eK9WL4&wx_screen_direc=portrait&wx_navbar_transparent=true&path=/p/exhibition/dippueokr/index.html&ncms_spm=a27aq.25248930&prefetchKey=exhibition&cardType=101001652&cardId=103000008047996&topOfferIds=1600199575147&templateBusinessCode=2021-11-01-jiajuyuanyizhanhui']

    def parse(self, response):
        print(response.xpath('//*[@id="4539339250"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/a/div[2]/div/div[1]/text()').get())
        print(response.xpath('//div[@class="word"]/text()').extract())