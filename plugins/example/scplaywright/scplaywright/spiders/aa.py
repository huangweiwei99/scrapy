from playwright.sync_api import Playwright, sync_playwright
def run(playwright: Playwright) -> None:
    browser = playwright.webkit.launch(headless=False)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to https://www.baidu.com/
    page.goto("https://www.baidu.com/")
    # Click text=学习六中全会精神 这些表述要精读
    with page.expect_popup() as popup_info:
        page.click("text=学习六中全会精神 这些表述要精读")
    page1 = popup_info.value
    # Click text=学习六中全会精神,这些表述要精读-新华网
    # with page1.expect_navigation(url="http://www.xinhuanet.com/politics/2021-11/19/c_1128080146.htm"):
    with page1.expect_navigation():
        with page1.expect_popup() as popup_info:
            page1.click("text=学习六中全会精神,这些表述要精读-新华网")
        page2 = popup_info.value
    # Click :nth-match(:text("财经"), 4)
    with page2.expect_popup() as popup_info:
        page2.click(":nth-match(:text(\"财经\"), 4)")
    page3 = popup_info.value
    # Click text=央广网
    with page3.expect_popup() as popup_info:
        page3.click("text=央广网")
    page4 = popup_info.value
    # ---------------------
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)

