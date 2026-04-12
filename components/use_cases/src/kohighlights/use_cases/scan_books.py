"""Use case: scan a directory and load Book objects.

Two entry points:
* :func:`scan_directory`   — live filesystem scan (generator-based, async-friendly)
* :func:`load_from_archive` — load books from the SQLite archive
"""
from __future__ import annotations

import re
from os.path import isfile, getmtime, splitext, basename
from datetime import datetime
from pathlib import Path
from typing import Callable, Generator

from kohighlights.file_scanner import scan_for_books, scan_from_db_records
from kohighlights.book_store import BookStore
from kohighlights.models import Book, Highlight


# ── Helpers ──────────────────────────────────────────────────────────────────


def _highlights_from_raw(raw: dict) -> list[Highlight]:
    """Extract Highlight objects from a raw Lua dict (read-only, no write-back)."""
    from kohighlights.file_scanner.scanner import _extract_highlights
    return _extract_highlights(raw)


# ── Use cases ─────────────────────────────────────────────────────────────────


def scan_directory(
    root: str,
    on_book_found: Callable[[Book], None],
    skip_paths: set[str] | None = None,
) -> int:
    """Scan *root* for KOReader metadata and call *on_book_found* for each book.

    Returns total number of books found.
    Skips paths in *skip_paths* (already loaded).
    """
    count = 0
    for book in scan_for_books(root, skip_paths=skip_paths):
        on_book_found(book)
        count += 1
    return count


def load_from_archive(store: BookStore) -> list[Book]:
    """Load all books from the archive database.

    Returns a list of :class:`~kohighlights.models.Book` objects.
    """
    return list(scan_from_db_records(store.all_records()))


def get_highlights_for_book(book: Book) -> list[Highlight]:
    """Extract and return all highlights for *book* from its raw_data."""
    return _highlights_from_raw(book.raw_data)


def get_all_highlights(books: list[Book]) -> list[Highlight]:
    """Return a flat list of all highlights across *books*."""
    result: list[Highlight] = []
    for book in books:
        highs = _highlights_from_raw(book.raw_data)
        # Attach book metadata to each highlight for the highlights-view table
        for h in highs:
            if not h.chapter and book.title:
                pass  # chapter comes from metadata; leave as-is
        result.extend(highs)
    return result
