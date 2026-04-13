"""Use case: archive, delete, and modify books."""
from __future__ import annotations

import json
import os
import shutil
from os.path import isfile, isdir, dirname
from pathlib import Path

from kohighlights.lua_codec import encode_file
from kohighlights.book_store import BookStore
from kohighlights.models import Book, Highlight


# ── Archive ───────────────────────────────────────────────────────────────────


def archive_books(
    books: list[Book],
    store: BookStore,
) -> tuple[int, int, int]:
    """Add selected books to the archive.

    Returns ``(added, skipped_no_highlights, skipped_old_format)``.
    """
    records: list[dict] = []
    empty = old = 0

    for book in books:
        if not book.highlights:
            empty += 1
            continue
        if not book.md5:
            old += 1
            continue
        raw = dict(book.raw_data)
        # Strip high-churn data that bloats the db needlessly
        raw.get("stats", {}).pop("performance_in_pages", None)
        raw.pop("page_positions", None)
        records.append({
            "md5": book.md5,
            "date": book.modified_date,
            "path": book.path,
            "data": raw,
        })

    added = store.upsert_many(records)
    return added, empty, old


# ── File deletion ─────────────────────────────────────────────────────────────


def delete_books_info(books: list[Book]) -> None:
    """Remove the ``.sdr`` metadata folder for each book."""
    for book in books:
        sdr = dirname(book.path)
        if sdr.endswith(".sdr") and isdir(sdr):
            shutil.rmtree(sdr, ignore_errors=True)
        elif isfile(book.path):
            os.remove(book.path)


def delete_books_and_files(books: list[Book]) -> None:
    """Remove both ``.sdr`` metadata and the actual book file."""
    for book in books:
        sdr = dirname(book.path)
        if sdr.endswith(".sdr") and isdir(sdr):
            shutil.rmtree(sdr, ignore_errors=True)
        elif isfile(book.path):
            os.remove(book.path)
        if book.book_path and isfile(book.book_path):
            os.remove(book.book_path)


def get_missing_books(books: list[Book]) -> list[Book]:
    """Return books whose actual book file no longer exists on disk."""
    return [b for b in books if b.book_path and not isfile(b.book_path)]


# ── Highlight editing ─────────────────────────────────────────────────────────


def delete_highlight(book: Book, highlight: Highlight) -> None:
    """Remove *highlight* from *book*'s raw_data and update the in-memory list.

    Caller must call :func:`save_book` afterward to persist the change.
    """
    raw_highs = book.raw_data.get("highlight", {})
    raw_bkms = book.raw_data.get("bookmarks", {})

    # Find and remove from raw highlight dict
    page_key = highlight.page
    for pid, h_data in list((raw_highs.get(page_key) or {}).items()):
        if h_data.get("text", "").replace("\\\n", "\n") == highlight.text:
            del raw_highs[page_key][pid]
            break

    # Remove associated bookmark (note/comment)
    if highlight.text:
        escaped = highlight.text.replace("\n", "\\\n")
        for idx in list(raw_bkms.keys()):
            if raw_bkms[idx].get("notes") == escaped:
                del raw_bkms[idx]
                break

    # Compact: remove empty page dicts
    for page in list(raw_highs.keys()):
        if not raw_highs[page]:
            del raw_highs[page]

    # Update in-memory Book model
    book.highlights = [h for h in book.highlights if h is not highlight]


def update_highlight_comment(book: Book, highlight: Highlight, new_comment: str) -> None:
    """Update the comment for *highlight* in *book*'s raw_data.

    Also updates the Highlight object in place.
    Caller must call :func:`save_book` afterward.
    """
    escaped_text = highlight.text.replace("\n", "\\\n")
    raw_bkms = book.raw_data.setdefault("bookmarks", {})

    for idx in raw_bkms:
        if raw_bkms[idx].get("notes") == escaped_text:
            raw_bkms[idx]["text"] = new_comment.replace("\n", "\\\n")
            break
    else:
        # No bookmark exists yet — create one
        new_idx = (max(raw_bkms.keys(), default=0) + 1) if raw_bkms else 1
        raw_bkms[new_idx] = {
            "notes": escaped_text,
            "text": new_comment.replace("\n", "\\\n"),
        }

    highlight.comment = new_comment


def save_book(book: Book) -> None:
    """Write *book*'s raw_data back to its ``.lua`` metadata file."""
    encode_file(book.path, dict(book.raw_data))
