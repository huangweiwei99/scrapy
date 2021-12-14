from pathlib import Path

import scrapy
from scrapy import cmdline, Request
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageCoroutine


class AlibabaSpider(scrapy.Spider):
    name = 'alibaba'

    def start_requests(self):
        yield Request(
            url="https://www.alibaba.com",
            # cookies={"foo": "bar"},
            meta={
                "playwright": True,
                "playwright_page_coroutines": [
                    PageCoroutine(
                        "screenshot", path=Path(__file__).parent / "ali2.png", full_page=True
                    ),
                ],
            },
        )

    def parse(self, response):
        return {"url": response.url}


# if __name__ == "__main__":
#     cmdline.execute(['scrapy', 'crawl', 'scroll'])
if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "PLAYWRIGHT_BROWSER_TYPE": "firefox",
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                # "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
        }
    )
    process.crawl(AlibabaSpider)
    process.start()
