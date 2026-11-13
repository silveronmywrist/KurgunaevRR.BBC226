import sqlite3
from contextlib import closing
from pathlib import Path


DB_PATH = Path(__file__).resolve().with_name("trips.db")


def create_database(path=DB_PATH):
    with closing(sqlite3.connect(path)) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS trips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    saved_at TEXT NOT NULL,
                    distance TEXT NOT NULL,
                    consumption TEXT NOT NULL,
                    price TEXT NOT NULL,
                    multiplier INTEGER NOT NULL CHECK (multiplier IN (1, 2)),
                    people INTEGER NOT NULL CHECK (people BETWEEN 1 AND 100),
                    total_distance TEXT NOT NULL,
                    fuel TEXT NOT NULL,
                    cost TEXT NOT NULL,
                    per_person TEXT NOT NULL
                )
            """)


if __name__ == "__main__":
    create_database()
    print(f"База данных готова: {DB_PATH}")
