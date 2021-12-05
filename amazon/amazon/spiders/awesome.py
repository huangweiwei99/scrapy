import scrapy


class AwesomeSpider(scrapy.Spider):
    name = 'awesome'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/']

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
        # 'response' contains the page as seen by the browser
        yield {"url": response.url}
