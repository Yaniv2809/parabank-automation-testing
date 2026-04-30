import allure
import pytest

from pages.loan_page import LoanPage


@pytest.mark.ui
@pytest.mark.high
class TestLoan:

    @allure.id("UI-009")
    @allure.title("Loan request — approved scenario")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_loan_approved(self, logged_in_page):
        """
        Small loan ($100) with a 50 % down payment ($50).  A small amount
        reduces balance dependency — ParaBank should approve regardless of
        how much other tests have spent.
        """
        lp = LoanPage(logged_in_page)
        lp.goto()
        lp.request_loan(amount="100", down_payment="50")
        assert lp.is_approved(), "Expected loan approval for $100 with $50 down payment"

    @allure.id("UI-010")
    @allure.title("Loan request — denied scenario")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_loan_denied(self, logged_in_page):
        """
        Very large loan ($100 000) with a token down payment ($1) → should be
        denied because the down payment ratio is far below ParaBank's threshold.
        """
        lp = LoanPage(logged_in_page)
        lp.goto()
        lp.request_loan(amount="100000", down_payment="1")
        assert lp.is_denied(), "Expected loan denial for $100 000 with only $1 down payment"
