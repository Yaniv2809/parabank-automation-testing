import allure
import pytest
from testaxiom import analyze

from pages.login_page import LoginPage
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD


@pytest.mark.ui
@pytest.mark.high
class TestLogin:

    @allure.id("UI-001")
    @allure.title("Valid login with default credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, page):
        lp = LoginPage(page)
        lp.goto()
        lp.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        assert lp.is_logged_in(), "Expected redirect to account overview after valid login"

    @allure.id("UI-002")
    @allure.title("Login with invalid password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_password(self, page):
        lp = LoginPage(page)
        lp.goto()
        lp.login(DEFAULT_USERNAME, "wrongpassword_xyz")
        assert not lp.is_logged_in(), "Should stay on login page after invalid password"
        assert lp.get_error_message(), "Expected an error message"

    @allure.id("UI-003")
    @allure.title("Login with empty username — BVA via TestAxiom")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_empty_username_bva(self, page):
        """
        TestAxiom generates EP partitions for a string parameter.
        The 'empty_string' partition must be classified as INVALID.
        We then execute that specific boundary value against the live UI.
        """
        analysis  = analyze("username", param_type="str")
        empty_tc  = next(tc for tc in analysis.test_cases if tc.partition == "empty_string")

        assert empty_tc.expected.value == "invalid", (
            f"TestAxiom rationale: {empty_tc.rationale}"
        )

        lp = LoginPage(page)
        lp.goto()
        lp.login(empty_tc.input_value, "")   # input_value == ''
        assert not lp.is_logged_in(), "Empty username must not allow login"
