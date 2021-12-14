import scrapy
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageCoroutine
from pathlib import Path


class ScrollSpider(scrapy.Spider):
    name = 'scroll'

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.alibaba.com/products/sofa.html?IndexArea=product_en&page=2",
            # meta=dict(
            #     playwright=True,
            #     playwright_include_page=True,
            #
            #     playwright_page_coroutines=[
            #         PageCoroutine("wait_for_selector", "title"),
            #         PageCoroutine(
            #             "screenshot", path=Path(__file__).parent / "alibaba.png", full_page=True
            #         ),
            #         # PageCoroutine("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
            #         # PageCoroutine("wait_for_selector", "div.list-no-v2-outter.J-offer-wrapper:nth-child(20)"),  # 10 per page
            #     ],
            # ),
            meta={
                "playwright": True,
                "playwright_context": "new",
                "playwright_context_kwargs": {
                    "java_script_enabled": False,
                    "ignore_https_errors": True,
                },
                # "playwright_include_page": True,
                "playwright_page_coroutines": [
                    PageCoroutine("wait_for_selector", "div.list-no-v2-outter.J-offer-wrapper"),
                    PageCoroutine("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    PageCoroutine("wait_for_selector", "div.list-no-v2-outter.J-offer-wrapper:nth-child(20)"),
                    PageCoroutine(
                        "screenshot", path=Path(__file__).parent / "alibaba.png", full_page=True
                    ),

                ],
            },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.screenshot(path="alibaba_scroll.png", full_page=True)
        await page.close()
        return {"quote_count": len(response.css("div.list-no-v2-outter.J-offer-wrapper"))}


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
            'PLAYWRIGHT_BROWSER_TYPE': 'firefox',
        }
    )
    process.crawl(ScrollSpider)
    process.start()
