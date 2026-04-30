from playwright.sync_api import Page
from pages.base_page import BasePage
from config.settings import BASE_URL


class LoanPage(BasePage):
    URL = f"{BASE_URL}/requestloan.htm"

    def __init__(self, page: Page):
        super().__init__(page)
        self.amount_input       = page.locator("input#amount")
        self.down_payment_input = page.locator("input#downPayment")
        self.from_account       = page.locator("select#fromAccountId")
        self.submit_button      = page.locator('input[value="Apply Now"]')

    def goto(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def request_loan(self, amount: str, down_payment: str, from_index: int = 0):
        self.amount_input.fill(str(amount))
        self.down_payment_input.fill(str(down_payment))
        self.from_account.select_option(index=from_index)
        self.submit_button.click()
        self.page.wait_for_load_state("networkidle")

    def is_approved(self) -> bool:
        return "Approved" in self.page.content()

    def is_denied(self) -> bool:
        return "Denied" in self.page.content()
