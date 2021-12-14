import scrapy
from scrapy import cmdline


class AwesomeSpider(scrapy.Spider):
    name = "awesome1"

    def start_requests(self):
        # GET request
        yield scrapy.Request("https://httpbin.org/get", meta={"playwright": True})
        # POST request
        yield scrapy.FormRequest(
            url="https://httpbin.org/post",
            formdata={"foo": "bar"},
            meta={"playwright": True},
        )

    def parse(self, response):
        print(response.url)
        # 'response' contains the page as seen by the browser
        yield {"url": response.url}


if __name__ == "__main__":
    cmdline.execute(['scrapy', 'crawl', 'awesome1'])
