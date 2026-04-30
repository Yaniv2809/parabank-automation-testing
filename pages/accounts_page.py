from playwright.sync_api import Page
from pages.base_page import BasePage
from config.settings import BASE_URL


class AccountsPage(BasePage):
    URL = f"{BASE_URL}/overview.htm"

    def __init__(self, page: Page):
        super().__init__(page)
        self.account_rows = page.locator("#accountTable tbody tr")

    def goto(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def has_accounts(self) -> bool:
        return self.account_rows.count() > 0

    def get_account_ids(self) -> list[str]:
        links = self.page.locator("#accountTable tbody tr td:first-child a")
        return [links.nth(i).inner_text().strip() for i in range(links.count())]

    def get_balance(self, row_index: int = 0) -> float:
        cell = self.account_rows.nth(row_index).locator("td").nth(1)
        raw  = cell.inner_text().replace("$", "").replace(",", "").strip()
        return float(raw)
