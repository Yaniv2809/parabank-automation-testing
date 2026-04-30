from playwright.sync_api import Page
from pages.base_page import BasePage
from config.settings import BASE_URL


class TransferPage(BasePage):
    URL = f"{BASE_URL}/transfer.htm"

    def __init__(self, page: Page):
        super().__init__(page)
        self.amount_input  = page.locator("input#amount")
        self.from_account  = page.locator("select#fromAccountId")
        self.to_account    = page.locator("select#toAccountId")
        self.submit_button = page.locator('input[value="Transfer"]')
        self.success_title = page.locator("h1.title")
        self.error_message = page.locator("p.error")

    def goto(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def transfer(self, amount: str, from_index: int = 0, to_index: int = 1):
        self.amount_input.fill(str(amount))
        self.from_account.select_option(index=from_index)
        self.to_account.select_option(index=to_index)
        self.submit_button.click()
        self.page.wait_for_load_state("networkidle")

    def is_success(self) -> bool:
        loc = self.success_title
        return loc.count() > 0 and "Transfer Complete" in loc.inner_text()

    def get_error(self) -> str:
        loc = self.error_message
        return loc.inner_text() if loc.count() > 0 else ""
