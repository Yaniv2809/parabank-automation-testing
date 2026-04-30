import os

BASE_URL = "https://parabank.parasoft.com/parabank"
API_BASE = f"{BASE_URL}/services/bank"

DEFAULT_USERNAME = "john"
DEFAULT_PASSWORD = "demo"

# Set PARABANK_DB_PATH to a SQLite file path when running against local Docker.
# Empty string = DB layer tests are skipped automatically.
DB_PATH = os.getenv("PARABANK_DB_PATH", "")

HEADLESS = os.getenv("HEADLESS", "true").lower() != "false"
