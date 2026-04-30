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
        # fromAccountId options are in the static HTML for loan page,
        # but wait_for_selector is defensive in case of slow loads.
        self.page.wait_for_selector("select#fromAccountId option", timeout=15_000)
        self.amount_input.fill(str(amount))
        self.down_payment_input.fill(str(down_payment))
        self.from_account.select_option(index=from_index)
        self.submit_button.click()
        # Result arrives via AJAX — wait for one of the result divs to appear.
        self.page.wait_for_selector(
            "#loanRequestApproved, #loanRequestDenied, #requestLoanError",
            state="visible",
            timeout=15_000,
        )

    def is_approved(self) -> bool:
        loc = self.page.locator("#loanRequestApproved")
        return loc.count() > 0 and loc.is_visible()

    def is_denied(self) -> bool:
        loc = self.page.locator("#loanRequestDenied")
        return loc.count() > 0 and loc.is_visible()
