import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess


class ExampleSpider(scrapy.Spider):
    name = 'detail'
    allowed_domains = ['1688.com']

    # start_urls = [
    #     'https://detail.1688.com/offer/657584057063.html?spm=a26352.13672862.offerlist.7.1cb73f3fftyYha']

    def start_requests(self):
        requesta = Request.from_curl(
            """curl 'https://detail.1688.com/offer/657584057063.html?spm=a26352.13672862.offerlist.7.1cb73f3fftyYha' \
  -H 'authority: detail.1688.com' \
  -H 'cache-control: max-age=0' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-user: ?1' \
  -H 'sec-fetch-dest: document' \
  -H 'referer: https://detail.1688.com/offer/657584057063.html?spm=a26352.13672862.offerlist.7.1cb73f3fftyYha' \
  -H 'accept-language: zh,zh-CN;q=0.9,en-GB;q=0.8,en;q=0.7' \
  -H 'cookie: _uab_collina=163767077412599860509228; cna=Z9E/GdjiQhgCAXFpybkR3TM5; _bl_uid=9kkXkw60cq22zewtydhFt5ea8kbs; taklid=8b81883a0f294d58994b76cfeb54c2a7; hng=CN%7Czh-CN%7CCNY%7C156; xlly_s=1; x5sec=7b226c61707574613b32223a226463626139663361633936336435646233643134656434616531626430376136434e6950724930474549362b3459574a76347159597a4432724b6b71227d; _csrf_token=1638598620077; _m_h5_tk=58e320e9005935c2399f7e491d3e1be7_1638608700108; _m_h5_tk_enc=8bff7d8337f28b7cea8b91a131960cea; JSESSIONID=FADEB71BF42198A6D78FAD0D4E4C7B2B; cookie2=137ff663e92784a2d53c13733785883a; t=d60d7c2996ad791e9b641fbbed966ef3; _tb_token_=f16b3670d3937; __cn_logon__=false; tfstk=cs1CB2ci3gCZoeyrTwaZ8ukeMJ91ZTl6uutORTCAUVEorF7Ciic2cZfpKDAyyF1..; l=eBrogEUmg4N4JSQCBOfwnurza77tIIRAguPzaNbMiOCPOI6v5JKdW6IGv-xJCnGNh6c9R3leTTyDBeYBc3xonxvTVeSBV3Mmn; isg=BFxcyBXKUcQ1tyWvOToskUmPLXwO1QD_8bmRgzZdbscqgfwLXuH_jjQz4eF5CThX' \
  --compressed"""
        )

        requesta.callback = self.parse

        yield requesta

    def parse(self, response):
        print(response.request.headers)
        title = response.xpath('//title/text()').get()
        print(title)


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                # "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
        }
    )
    process.crawl(ExampleSpider)
    process.start()
