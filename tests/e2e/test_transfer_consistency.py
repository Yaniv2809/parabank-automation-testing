import allure
import pytest

from pages.transfer_page import TransferPage
from utils.db_connector import fetch_last_transaction, fetch_account_balance


@pytest.mark.e2e
@pytest.mark.high
class TestTransferConsistency:

    @allure.id("E2E-001")
    @allure.title("Transfer via UI → verify API balance → confirm DB record")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_transfer_full_stack(self, logged_in_page, api_client, john_accounts, db):
        """
        Cross-layer integrity check:
          1. UI  — execute a $1 transfer
          2. API — verify 'from' account balance decreased by $1
          3. DB  — confirm a transaction record exists (skipped if DB unavailable)
        """
        from_id, to_id = john_accounts[0], john_accounts[1]
        amount = 1.00

        # ── 1. Get pre-transfer balance via API ──────────────────────────────
        pre_balance = api_client.get_account(from_id).json()["balance"]

        # ── 2. Execute transfer through the UI ──────────────────────────────
        with allure.step("UI: execute $1 transfer"):
            tp = TransferPage(logged_in_page)
            tp.goto()
            tp.transfer(amount=str(amount))
            assert tp.is_success(), "UI: expected 'Transfer Complete' heading"

        # ── 3. Verify balance change via API ─────────────────────────────────
        with allure.step("API: verify balance decreased by $1"):
            post_balance = api_client.get_account(from_id).json()["balance"]
            assert abs((pre_balance - post_balance) - amount) < 0.01, (
                f"API: balance should have dropped by ${amount:.2f}. "
                f"Before={pre_balance:.2f} After={post_balance:.2f}"
            )

        # ── 4. Verify via API transaction history (proxy for DB) ─────────────
        with allure.step("API: transaction appears in history"):
            txns = api_client.get_transactions(from_id).json()
            assert any(
                abs(t.get("amount", 0)) == amount for t in txns
            ), "API: no transaction record found for the $1 transfer"

        # ── 5. Optional: direct DB verification ──────────────────────────────
        if db is None:
            pytest.skip("DB layer not configured — set PARABANK_DB_PATH for local Docker runs")

        with allure.step("DB: last transaction record exists"):
            row = fetch_last_transaction(db, from_id)
            assert row is not None, "DB: no transaction row found for the transfer"

        with allure.step("DB: account balance matches API"):
            db_balance = fetch_account_balance(db, from_id)
            assert abs(db_balance - post_balance) < 0.01, (
                f"DB balance {db_balance:.2f} != API balance {post_balance:.2f}"
            )
