import sys
import os

# Must run before any FixtureForge import to prevent UnicodeEncodeError on Windows.
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import pytest
from playwright.sync_api import Page

from api_clients.bank_api_client import BankAPIClient
from utils.db_connector import get_connection
from utils.fixture_forge_engine import create_forge
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD


# ── API client ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def api_client() -> BankAPIClient:
    client = BankAPIClient()
    client.login()
    return client


@pytest.fixture(scope="session")
def john_accounts(api_client: BankAPIClient) -> list[int]:
    return [acc["id"] for acc in api_client.accounts]


# ── Database ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def db():
    conn = get_connection()
    yield conn
    if conn:
        conn.close()


# ── FixtureForge ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def forge():
    return create_forge(seed=42)


# ── Playwright — reduce default timeout from 30 s → 15 s ─────────────────────
# Override the pytest-playwright `page` fixture so the shorter timeouts apply
# to every UI test automatically — WITHOUT autouse (which would wrongly inject
# a Playwright browser into pure-API tests and add 30-40 s overhead per test).

@pytest.fixture
def page(page: Page) -> Page:  # type: ignore[override]
    page.set_default_timeout(15_000)
    page.set_default_navigation_timeout(20_000)
    return page


# ── UI — pre-logged-in page ───────────────────────────────────────────────────

@pytest.fixture
def logged_in_page(page: Page) -> Page:
    from pages.login_page import LoginPage
    lp = LoginPage(page)
    lp.goto()
    lp.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
    return page
