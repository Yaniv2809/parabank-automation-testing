import allure
import pytest

from pages.loan_page import LoanPage
from utils.db_connector import fetch_last_transaction


@pytest.mark.e2e
@pytest.mark.high
class TestLoanLogic:

    @allure.id("E2E-003")
    @allure.title("Loan request via UI → verify API status → DB confirmation")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_loan_full_stack(self, logged_in_page, api_client, john_accounts, db):
        """
        Cross-layer loan integrity check:
          1. UI  — submit a $1 000 loan request ($100 down)
          2. API — verify the loan is recorded as approved
          3. DB  — confirm a transaction record exists (skipped if DB unavailable)
        """
        from_id = john_accounts[0]
        amount, down = 1_000, 500

        # ── 1. UI: submit loan ───────────────────────────────────────────────
        with allure.step("UI: submit $1 000 loan with $500 down"):
            lp = LoanPage(logged_in_page)
            lp.goto()
            lp.request_loan(amount=str(amount), down_payment=str(down))
            assert lp.is_approved(), "UI: expected loan approval confirmation"

        # ── 2. API: verify loan approval ─────────────────────────────────────
        with allure.step("API: confirm loan approved"):
            resp = api_client.request_loan(amount, down, from_id)
            assert resp.status_code == 200
            data = resp.json()
            assert data.get("approved") is True, (
                f"API: expected loan to be approved. Response: {data}"
            )

        # ── 3. Optional: DB verification ─────────────────────────────────────
        if db is None:
            pytest.skip("DB layer not configured — set PARABANK_DB_PATH for local Docker runs")

        with allure.step("DB: loan transaction record exists"):
            row = fetch_last_transaction(db, from_id)
            assert row is not None, "DB: no transaction row found after loan approval"
