import scrapy
from scrapy import cmdline
from scrapy_playwright.page import PageCoroutine


class PdfSpider(scrapy.Spider):
    name = 'pdf'

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.baidu.com",
            meta=dict(
                playwright=True,
                playwright_page_coroutines={
                    "click": PageCoroutine("click", selector="a"),
                    "pdf": PageCoroutine("pdf", path="/tmp/file.pdf"),
                },
            ),
        )

    def parse(self, response):
        pdf_bytes = response.meta["playwright_page_coroutines"]["pdf"].result
        with open("baidu.pdf", "wb") as fp:
            fp.write(pdf_bytes)
        yield {"url": response.url}


if __name__ == "__main__":
    cmdline.execute(['scrapy', 'crawl', 'pdf'])
