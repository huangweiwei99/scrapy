from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.webkit.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.1688.com/
    page.goto("https://www.1688.com/")

    # Click [placeholder="搜索 商品/供应商/求购"]
    page.click("[placeholder=\"搜索 商品/供应商/求购\"]")

    # Fill [placeholder="搜索 商品/供应商/求购"]
    page.fill("[placeholder=\"搜索 商品/供应商/求购\"]", "Shafa ")

    # Click [placeholder="搜索 商品/供应商/求购"]
    page.click("[placeholder=\"搜索 商品/供应商/求购\"]")

    # Fill [placeholder="搜索 商品/供应商/求购"]
    page.fill("[placeholder=\"搜索 商品/供应商/求购\"]", "沙发")

    # Click text=意式极简真皮沙发轻奢沙发客厅头层牛皮现代简约北欧沙发组合套装免费赊账¥1380成交1万+元2年佛山市雅之欧家具有限公司广告 >> a div
    with page1.expect_popup() as popup_info:
        page1.click("text=意式极简真皮沙发轻奢沙发客厅头层牛皮现代简约北欧沙发组合套装免费赊账¥1380成交1万+元2年佛山市雅之欧家具有限公司广告 >> a div")
    page2 = popup_info.value

    # Close page
    page1.close()

    # Close page
    page.close()

    # Close page
    page2.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
