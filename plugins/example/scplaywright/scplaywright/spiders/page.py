import scrapy
from scrapy import cmdline


class PageSpider(scrapy.Spider):
    name = "page"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.baidu.com",
            meta={"playwright": True, "playwright_include_page": True},
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        title = await page.title()  # "百度一下，你就知道"
        await page.close()
        return {"title": title}


if __name__ == "__main__":
    cmdline.execute(['scrapy', 'crawl', 'page'])
