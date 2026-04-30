from playwright.sync_api import Page
from pages.base_page import BasePage
from config.settings import BASE_URL


class LoginPage(BasePage):
    URL = f"{BASE_URL}/index.htm"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator('input[name="username"]')
        self.password_input = page.locator('input[name="password"]')
        self.login_button   = page.locator('input[value="Log In"]')
        self.error_message  = page.locator("p.error")

    def goto(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_error_message(self) -> str:
        loc = self.error_message
        return loc.inner_text() if loc.count() > 0 else ""

    def is_logged_in(self) -> bool:
        # ParaBank redirects to overview.htm for BOTH success AND failure.
        #
        # ❌ Cannot use p.error: it lives inside div#showError (display:none)
        #    which is always present in the DOM — locator.count() includes
        #    hidden elements, so it is always > 0.
        #
        # ✅ Use a[href="logout.htm"]: rendered server-side in the leftPanel
        #    Account Services menu. Present only for authenticated sessions,
        #    unaffected by the right-panel AJAX account loader.
        if "overview" not in self.page.url:
            return False
        return self.page.locator('a[href="logout.htm"]').count() > 0
