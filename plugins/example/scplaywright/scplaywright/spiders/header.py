from pathlib import Path

from scrapy import Spider, Request, cmdline
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


# from plugins.example.scplaywright.scplaywright.middlewares import


class HeaderSpider(Spider):
    """
    Send random header
    """

    name = "header"

    def start_requests(self):
        yield Request(
            url="https://httpbin.org",
            # meta={
            #     "playwright": True,
            #     # "playwright_page_coroutines": [
            #     #     PageCoroutine(
            #     #         "screenshot", path=Path(__file__).parent / "cookies.png", full_page=True
            #     #     ),
            #     # ],
            # },
        )

    def parse(self, response):
        print(response.request.headers)
        print({"User-Agent": response.request.headers['User-Agent']})


if __name__ == "__main__":
    print(get_project_settings())
    process = CrawlerProcess(
        # get_project_settings()
        settings={
            # "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            # "DOWNLOAD_HANDLERS": {
            #     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            #     # "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            # },
            'DOWNLOADER_MIDDLEWARES': {
                # 'scplaywright.middlewares.ScplaywrightDownloaderMiddleware': 543,
                'scplaywright.middlewares.RandomUserAgentMiddleware': 543,
            }
        }
    )
    process.crawl(HeaderSpider)
    process.start()

    # cmdline.execute(['scrapy', 'crawl', 'header',
    #                  # '-o', '{0}_{1}.json'.format('luxurylivinggroup', today)
    #                  ])
