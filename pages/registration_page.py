from playwright.sync_api import Page
from pages.base_page import BasePage
from config.settings import BASE_URL


class RegistrationPage(BasePage):
    URL = f"{BASE_URL}/register.htm"

    def goto(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def register(
        self,
        first_name:  str,
        last_name:   str,
        address:     str,
        city:        str,
        state:       str,
        zip_code:    str,
        phone:       str,
        ssn:         str,
        username:    str,
        password:    str,
    ):
        p = self.page
        p.fill('[id="customer.firstName"]',        first_name)
        p.fill('[id="customer.lastName"]',         last_name)
        p.fill('[id="customer.address.street"]',   address)
        p.fill('[id="customer.address.city"]',     city)
        p.fill('[id="customer.address.state"]',    state)
        p.fill('[id="customer.address.zipCode"]',  zip_code)
        p.fill('[id="customer.phoneNumber"]',      phone)
        p.fill('[id="customer.ssn"]',              ssn)
        p.fill('[id="customer.username"]',         username)
        p.fill('[id="customer.password"]',         password)
        p.fill('[id="repeatedPassword"]',          password)
        p.click('input[value="Register"]')
        p.wait_for_load_state("networkidle")

    def is_registered(self) -> bool:
        return "Welcome" in self.page.content()

    def get_error(self) -> str:
        errors = self.page.locator("span.error")
        count  = errors.count()
        return " | ".join(errors.nth(i).inner_text() for i in range(count)) if count else ""
