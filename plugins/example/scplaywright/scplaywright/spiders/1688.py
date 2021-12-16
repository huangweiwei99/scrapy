import scrapy
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageCoroutine
from pathlib import Path


class Ali1688Spider(scrapy.Spider):
    name = 'scroll'

    def start_requests(self):
        yield scrapy.Request(
            url="https://detail.1688.com/offer/630771236405.html",
            meta={"playwright": True,
                  "playwright_include_page": True,
                  "playwright_context_kwargs": {
                      "java_script_enabled": True,
                      "ignore_https_errors": True,
                  },
                  },
        )

    # def parse(self, response):
    #     print(response.xpath('//title/text()').get())
    #     print(response.request.headers)
    #     # print(len(response.css("div.list-no-v2-outter.J-offer-wrapper")))
    #     # page = response.meta["playwright_page"]
    #     # await page.screenshot(path="alibaba_scroll.png", full_page=True)
    #     # await page.close()
    #     # return {"quote_count": len(response.css("div.list-no-v2-outter.J-offer-wrapper"))}
    async def parse(self, response):
        page = response.meta["playwright_page"]
        title = await page.title()  # "Example Domain"
        await page.close()
        return {"title": title}


# if __name__ == "__main__":
#     cmdline.execute(['scrapy', 'crawl', 'scroll'])

if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                # "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            'DOWNLOADER_MIDDLEWARES': {
                # 'scplaywright.middlewares.ScplaywrightDownloaderMiddleware': 543,
                # 'scplaywright.scplaywright.middlewares.RandomUserAgentMiddleware': 543,
            },
            'AUTOTHROTTLE_ENABLED': True,
            'AUTOTHROTTLE_START_DELAY': 1,
            'AUTOTHROTTLE_MAX_DELAY': 3,
            'DOWNLOAD_DELAY': 3
            # 'PLAYWRIGHT_BROWSER_TYPE': 'firefox',
        }
    )
    process.crawl(Ali1688Spider)
    process.start()
