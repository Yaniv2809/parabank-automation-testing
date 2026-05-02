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
# Cuts per-test wall-time in half when the public ParaBank server is slow or
# unresponsive, which is the main cause of 9-minute CI runs.

@pytest.fixture(autouse=True)
def _set_playwright_timeout(page: Page) -> None:
    page.set_default_timeout(15_000)
    page.set_default_navigation_timeout(20_000)


# ── UI — pre-logged-in page ───────────────────────────────────────────────────

@pytest.fixture
def logged_in_page(page: Page) -> Page:
    from pages.login_page import LoginPage
    lp = LoginPage(page)
    lp.goto()
    lp.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
    return page
