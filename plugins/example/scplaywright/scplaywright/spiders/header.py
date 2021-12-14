from pathlib import Path

from scrapy import Spider, Request, cmdline
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


# from plugins.example.scplaywright.scplaywright.middlewares import
from scrapy_playwright.page import PageCoroutine


class HeaderSpider(Spider):
    """
    Send random header
    """

    name = "header"

    def start_requests(self):
        yield Request(
            url="https://www.alibaba.com/products/sofa.html?IndexArea=product_en&page=2",
            meta={
                "playwright": True,
                "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                },
                # "playwright_include_page": True,
                "playwright_page_coroutines": [
                    PageCoroutine("wait_for_selector", "div.list-no-v2-outter.J-offer-wrapper"),
                    PageCoroutine("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    # PageCoroutine("wait_for_selector", "#root > div > div.app-organic-search__main-body > div.app-organic-search__content > div > div > div > div:nth-child(9)"),
                    PageCoroutine(
                        "screenshot", path=Path(__file__).parent / "alibaba.png", full_page=True
                    ),
                ],
            },
        )

    def parse(self, response):
        print(response.xpath('//title/text()').get())
        print(response.request.headers)
        print(len(response.css("div.list-no-v2-outter.J-offer-wrapper")))
        print({"User-Agent": response.request.headers['User-Agent']})


if __name__ == "__main__":
    process = CrawlerProcess(
        # get_project_settings()
        settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                # "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            'DOWNLOADER_MIDDLEWARES': {
                # 'scplaywright.middlewares.ScplaywrightDownloaderMiddleware': 543,
                # 'scplaywright.middlewares.RandomUserAgentMiddleware': 543,
            },
            # 'PLAYWRIGHT_BROWSER_TYPE':'firefox',
        }
    )
    process.crawl(HeaderSpider)
    process.start()

