"""SQLite-backed archive for KOReader book metadata.

Stores serialised book dicts so highlights can be browsed offline,
independently of the device being connected.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterator


_CREATE_SQL = """
CREATE TABLE IF NOT EXISTS books (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    md5     TEXT    UNIQUE NOT NULL,
    date    TEXT,
    path    TEXT,
    data    TEXT
);
"""

_UPSERT_SQL = """
INSERT INTO books (md5, date, path, data)
VALUES (?, ?, ?, ?)
ON CONFLICT(md5) DO UPDATE SET
    date = excluded.date,
    path = excluded.path,
    data = excluded.data;
"""


class BookStore:
    """Thin wrapper around the ``books`` SQLite table."""

    def __init__(self, db_path: str | Path) -> None:
        self._path = Path(db_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self._path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(_CREATE_SQL)
        self._conn.commit()

    # ── Write ────────────────────────────────────────────────────────────

    def upsert(self, md5: str, path: str, date: str, data: dict) -> None:
        """Insert or update a book record."""
        self._conn.execute(_UPSERT_SQL, (md5, date, path, json.dumps(data)))
        self._conn.commit()

    def upsert_many(self, records: list[dict]) -> int:
        """Bulk upsert.  Each record must have keys: md5, path, date, data (dict)."""
        rows = [(r["md5"], r["date"], r["path"], json.dumps(r["data"])) for r in records]
        self._conn.executemany(_UPSERT_SQL, rows)
        self._conn.commit()
        return len(rows)

    def delete(self, md5: str) -> None:
        self._conn.execute("DELETE FROM books WHERE md5 = ?", (md5,))
        self._conn.commit()

    # ── Read ─────────────────────────────────────────────────────────────

    def all_records(self) -> Iterator[tuple[str, str, str, dict]]:
        """Yield (md5, path, date, data_dict) for every archived book."""
        cur = self._conn.execute("SELECT md5, path, date, data FROM books")
        for row in cur:
            yield row["md5"], row["path"], row["date"], json.loads(row["data"])

    def get_by_md5(self, md5: str) -> dict | None:
        cur = self._conn.execute("SELECT data FROM books WHERE md5 = ?", (md5,))
        row = cur.fetchone()
        return json.loads(row["data"]) if row else None

    def count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]

    # ── Maintenance ──────────────────────────────────────────────────────

    def vacuum(self) -> None:
        self._conn.execute("VACUUM")

    def close(self) -> None:
        self._conn.close()

    # ── Context manager ──────────────────────────────────────────────────

    def __enter__(self) -> "BookStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
