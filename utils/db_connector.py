import sqlite3
from config.settings import DB_PATH


def get_connection() -> sqlite3.Connection | None:
    """Returns a SQLite connection when PARABANK_DB_PATH is set, else None.

    When None, DB-layer tests should call pytest.skip().
    """
    if not DB_PATH:
        return None
    return sqlite3.connect(DB_PATH)


def fetch_account_balance(conn: sqlite3.Connection, account_id: int) -> float | None:
    cur = conn.cursor()
    cur.execute("SELECT balance FROM ACCOUNT WHERE id = ?", (account_id,))
    row = cur.fetchone()
    return float(row[0]) if row else None


def fetch_last_transaction(conn: sqlite3.Connection, account_id: int) -> tuple | None:
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM TRANSACTION WHERE accountId = ? ORDER BY date DESC LIMIT 1",
        (account_id,),
    )
    return cur.fetchone()


def fetch_transaction_by_id(conn: sqlite3.Connection, transaction_id: int) -> tuple | None:
    cur = conn.cursor()
    cur.execute("SELECT * FROM TRANSACTION WHERE id = ?", (transaction_id,))
    return cur.fetchone()
