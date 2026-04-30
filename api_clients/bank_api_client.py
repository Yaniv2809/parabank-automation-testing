import requests
from config.settings import API_BASE, DEFAULT_USERNAME, DEFAULT_PASSWORD

_JSON = {"Accept": "application/json"}


class BankAPIClient:
    def __init__(self, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD):
        self.username    = username
        self.password    = password
        self.auth        = (username, password)
        self.customer_id: int | None = None
        self.accounts: list[dict]    = []

    # ── Auth ──────────────────────────────────────────────────────────────────

    def login(self) -> dict:
        resp = self._get(f"/login/{self.username}/{self.password}", auth=False)
        resp.raise_for_status()
        data = resp.json()
        self.customer_id = data["id"]
        self._refresh_accounts()
        return data

    def _refresh_accounts(self) -> list[dict]:
        resp = self._get(f"/customers/{self.customer_id}/accounts")
        resp.raise_for_status()
        self.accounts = resp.json()
        return self.accounts

    # ── Low-level HTTP ────────────────────────────────────────────────────────

    def _get(self, path: str, auth: bool = True, **kwargs) -> requests.Response:
        return requests.get(
            API_BASE + path,
            headers=_JSON,
            auth=self.auth if auth else None,
            **kwargs,
        )

    def _post(self, path: str, params: dict | None = None, auth: bool = True, **kwargs) -> requests.Response:
        return requests.post(
            API_BASE + path,
            headers=_JSON,
            auth=self.auth if auth else None,
            params=params,
            **kwargs,
        )

    # ── Banking operations ────────────────────────────────────────────────────

    def get_account(self, account_id: int) -> requests.Response:
        return self._get(f"/accounts/{account_id}")

    def get_customer_accounts(self) -> requests.Response:
        return self._get(f"/customers/{self.customer_id}/accounts")

    def transfer(self, from_id: int, to_id: int, amount: float) -> requests.Response:
        return self._post("/transfer", params={
            "fromAccountId": from_id,
            "toAccountId":   to_id,
            "amount":        amount,
        })

    def request_loan(self, amount: float, down_payment: float, from_id: int) -> requests.Response:
        return self._post("/requestLoan", params={
            "customerId":  self.customer_id,
            "amount":      amount,
            "downPayment": down_payment,
            "fromAccountId": from_id,
        })

    def get_transactions(self, account_id: int) -> requests.Response:
        return self._get(f"/accounts/{account_id}/transactions")

    def get_transactions_by_amount(self, account_id: int, amount: float) -> requests.Response:
        return self._get(f"/accounts/{account_id}/transactions/amount/{amount}")

    def get_customer(self, customer_id: int | None = None) -> requests.Response:
        cid = customer_id or self.customer_id
        return self._get(f"/customers/{cid}")

    def register(self, **kwargs) -> requests.Response:
        return self._post("/register", params=kwargs, auth=False)
