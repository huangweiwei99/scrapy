import json

import scrapy
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess


class PageSpider(scrapy.Spider):
    name = "page"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.baidu.com",
            meta={"playwright": True,
                  "playwright_include_page": True

                  },

        )

    async def parse(self, response):
        # page = response.meta["playwright_page"]
        # title = await page.title()  # "百度一下，你就知道"
        # await page.close()
        # return {"title": title}
        page = response.meta["playwright_page"]
        print(json.dumps({"url": response.url, "storage_state": await page.context.storage_state()}))
        return {"url": response.url, "storage_state": await page.context.storage_state()}


# if __name__ == "__main__":
#     cmdline.execute(['scrapy', 'crawl', 'page'])
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
    process.crawl(PageSpider)
    process.start()
