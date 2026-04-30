import allure
import pytest

from pages.accounts_page import AccountsPage


@pytest.mark.ui
@pytest.mark.high
class TestAccounts:

    @allure.id("UI-004")
    @allure.title("Account overview displays correct balance — UI matches API")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_balance_matches_api(self, logged_in_page, api_client, john_accounts):
        ap = AccountsPage(logged_in_page)
        ap.goto()

        assert ap.has_accounts(), "Account table must contain at least one row"

        ui_balance  = ap.get_balance(row_index=0)

        resp        = api_client.get_account(john_accounts[0])
        resp.raise_for_status()
        api_balance = resp.json()["balance"]

        assert abs(ui_balance - api_balance) < 0.01, (
            f"UI balance ${ui_balance:.2f} != API balance ${api_balance:.2f}"
        )
