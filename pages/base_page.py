from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def wait_for_text(self, text: str, timeout: int = 10_000):
        self.page.wait_for_function(
            f"() => document.body.innerText.includes({repr(text)})",
            timeout=timeout,
        )

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()
