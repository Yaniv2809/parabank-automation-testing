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
        url = self.page.url
        return "overview" in url or "accounts.htm" in url
