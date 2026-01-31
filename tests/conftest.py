import sqlite3
import pytest


def _create_test_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS sailboat_prices")
    cur.execute("""
        CREATE TABLE sailboat_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            cabins TEXT,
            berths INTEGER,
            length INTEGER,
            price_euro INTEGER,
            boat_type TEXT,
            country TEXT,
            region TEXT
        )
    """)

    # deterministic test dataset
    rows = [
        ("2025-07-06", "3", 6, 12, 10000, "Sailing yachts", "Croatia", "Split"),
        ("2025-07-13", "3", 6, 12, 12000, "Sailing yachts", "Croatia", "Split"),
        ("2025-07-20", "4", 8, 14, 15000, "Sailing yachts", "Croatia", "Split"),
        ("2025-07-13", "3", 6, 12, 8000,  "Sailing yachts", "Croatia", "Zadar"),
        ("2025-06-15", "3", 6, 12, 7000,  "Sailing yachts", "Croatia", "Split"),
        ("2025-07-13", "4", 8, 14, 20000, "Catamarans", "Croatia", "Split"),
    ]

    cur.executemany("""
        INSERT INTO sailboat_prices
        (date, cabins, berths, length, price_euro, boat_type, country, region)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()


@pytest.fixture(scope="session")
def test_db(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("db") / "test_finaldatabase_data.db"
    _create_test_db(str(db_file))
    return str(db_file)


@pytest.fixture(autouse=True)
def _set_db_path_env(monkeypatch, test_db):
    monkeypatch.setenv("DB_PATH", test_db)
