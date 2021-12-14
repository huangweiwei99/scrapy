import scrapy
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageCoroutine


class ScrollSpider(scrapy.Spider):
    name = 'scroll'

    def start_requests(self):
        yield scrapy.Request(
            url="http://quotes.toscrape.com/scroll",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_coroutines=[
                    PageCoroutine("wait_for_selector", "div.quote"),
                    PageCoroutine("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    PageCoroutine("wait_for_selector", "div.quote:nth-child(11)"),  # 10 per page
                ],
            ),
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.screenshot(path="scroll.png", full_page=True)
        await page.close()
        return {"quote_count": len(response.css("div.quote"))}


# if __name__ == "__main__":
#     cmdline.execute(['scrapy', 'crawl', 'scroll'])

if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                # "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
        }
    )
    process.crawl(ScrollSpider)
    process.start()
