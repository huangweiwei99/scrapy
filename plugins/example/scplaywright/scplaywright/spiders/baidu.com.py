import scrapy
import playwright
from scrapy.crawler import CrawlerProcess


class BaiduSpiderWithPage(scrapy.Spider):
    name = "page"

    def start_requests(self):
        yield scrapy.Request(
            url="https://detail.1688.com/offer/640795000660.html",
            meta={"playwright": True,
                  "playwright_include_page": True,
                  "playwright_context_kwargs": {
                      "java_script_enabled": True,
                      "ignore_https_errors": True,
                    },
                  },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        title = await page.title()  # "Example Domain"
        await page.close()
        return {"title": title}


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
    process.crawl(BaiduSpiderWithPage)
    process.start()
