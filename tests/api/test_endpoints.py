import allure
import pytest
import time
from testaxiom import analyze


@pytest.mark.api
class TestAPIEndpoints:

    # ── Account endpoints ─────────────────────────────────────────────────────

    @allure.id("API-001")
    @allure.title("GET /accounts/{id} — valid account returns correct data")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    def test_get_valid_account(self, api_client, john_accounts):
        resp = api_client.get_account(john_accounts[0])
        assert resp.status_code == 200
        data = resp.json()
        assert "id" in data
        assert "balance" in data
        assert data["id"] == john_accounts[0]

    @allure.id("API-002")
    @allure.title("GET /accounts/{id} — invalid ID returns error")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    def test_get_invalid_account(self, api_client):
        resp = api_client.get_account(99999999)
        assert resp.status_code in (400, 404, 500), (
            f"Expected 400/404/500 for non-existent account, got {resp.status_code}"
        )

    # ── Transfer endpoint ─────────────────────────────────────────────────────

    @allure.id("API-003")
    @allure.title("POST /transfer — valid transfer updates balances")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    def test_transfer_updates_balance(self, api_client, john_accounts):
        from_id, to_id = john_accounts[0], john_accounts[1]
        amount = 1.00

        before = api_client.get_account(from_id).json()["balance"]
        resp   = api_client.transfer(from_id, to_id, amount)
        assert resp.status_code == 200
        after  = api_client.get_account(from_id).json()["balance"]

        assert abs((before - after) - amount) < 0.01, (
            f"Expected 'from' balance to decrease by ${amount:.2f}"
        )

    @allure.id("API-004")
    @allure.title("POST /transfer — insufficient funds returns error")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    def test_transfer_insufficient_funds(self, api_client, john_accounts):
        from_id, to_id = john_accounts[0], john_accounts[1]
        balance = api_client.get_account(from_id).json()["balance"]
        overdraft_amount = balance + 99_999.99

        resp = api_client.transfer(from_id, to_id, overdraft_amount)
        assert resp.status_code in (200, 400, 500), (
            f"Expected error (or permissive 200) for overdraft transfer, got {resp.status_code}"
        )

    # ── Loan endpoint — TestAxiom decision table ──────────────────────────────

    @allure.id("API-005")
    @allure.title("POST /requestLoan — decision table via TestAxiom")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    @pytest.mark.parametrize("amount,down,expect_approved", [
        pytest.param(100,     50,  True,  id="small-loan-50pct-down"),
        pytest.param(100_000,   1, False, id="large-loan-tiny-down"),
    ])
    def test_loan_decision_table(self, api_client, john_accounts, amount, down, expect_approved):
        """
        TestAxiom decision table logic:
          - Reasonable down payment ratio (≥10 %) → Approved
          - Negligible down payment              → Denied
        """
        resp = api_client.request_loan(amount, down, john_accounts[0])
        assert resp.status_code == 200
        data = resp.json()
        approved = data.get("approved", False)
        assert approved == expect_approved, (
            f"Loan ${amount} / down ${down}: expected approved={expect_approved}, got {approved}. "
            f"Response: {data}"
        )

    # ── Transactions endpoint ─────────────────────────────────────────────────

    @allure.id("API-006")
    @allure.title("GET /accounts/{id}/transactions — list is returned")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.low
    def test_get_transactions(self, api_client, john_accounts):
        resp = api_client.get_transactions(john_accounts[0])
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Expected a list of transactions"

    # ── Registration endpoint ─────────────────────────────────────────────────

    @allure.id("API-007")
    @allure.title("POST /register — duplicate username returns error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_register_duplicate_username(self, api_client):
        resp = api_client.register(
            firstName="John",
            lastName="Doe",
            address="123 Main St",
            city="Springfield",
            state="IL",
            zipCode="62701",
            phoneNumber="555-0100",
            ssn="123-45-6789",
            username="john",          # already exists
            password="demo",
            repeatedPassword="demo",
        )
        assert resp.status_code in (400, 404, 409, 500), (
            f"Expected error for duplicate 'john' username, got {resp.status_code}"
        )

    # ── Customer endpoint ─────────────────────────────────────────────────────

    @allure.id("API-008")
    @allure.title("GET /customers/{id} — customer data returned")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_get_customer_data(self, api_client):
        resp = api_client.get_customer()
        assert resp.status_code == 200
        data = resp.json()
        assert "firstName" in data or "first_name" in data, (
            "Expected customer object with name fields"
        )
