"""Merge and sync KOReader highlights across multiple device copies.

When you read the same book on two devices, each may have different highlights
and reading positions.  This module provides two operations:

* :func:`merge_books`  — combine highlights from both copies, deduplicating by
  ``page_id`` (KOReader's internal position identifier).
* :func:`sync_books`   — copy the furthest reading position from one copy to
  the other, without touching highlights.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from kohighlights.lua_codec import encode_file
from kohighlights.models import Book, Highlight


# ── Result types ─────────────────────────────────────────────────────────────


@dataclass
class MergeResult:
    """Outcome of a merge or sync operation."""

    added: int = 0          # highlights added
    duplicates: int = 0     # highlights that were already present
    saved_paths: list[str] = None  # paths of .lua files that were written

    def __post_init__(self) -> None:
        if self.saved_paths is None:
            self.saved_paths = []


# ── Compatibility checks ──────────────────────────────────────────────────────


def same_book(book_a: Book, book_b: Book) -> bool:
    """Return True if both books represent the same text content.

    KOReader uses ``cre_dom_version`` to track the rendered DOM; highlights
    are only comparable when the DOM version is identical.
    """
    if not book_a.title or not book_b.title:
        return False
    titles_match = book_a.title.lower().strip() == book_b.title.lower().strip()
    cre_match = book_a.cre_dom_version == book_b.cre_dom_version
    return titles_match and cre_match


# ── Deduplication helpers ─────────────────────────────────────────────────────


def _highlight_key(h: Highlight) -> str:
    """Stable identity key for deduplication.

    Uses ``page_id`` when available (most reliable), falls back to the
    combination of page + first 60 chars of text.
    """
    if h.page_id:
        return h.page_id
    return f"{h.page}|{h.text[:60]}"


def _dedup(highlights: list[Highlight]) -> list[Highlight]:
    seen: set[str] = set()
    result: list[Highlight] = []
    for h in highlights:
        key = _highlight_key(h)
        if key not in seen:
            seen.add(key)
            result.append(h)
    return result


# ── Core operations ───────────────────────────────────────────────────────────


def merge_books(book_a: Book, book_b: Book) -> MergeResult:
    """Merge highlights from *book_b* into *book_a* (and vice versa) in-place.

    After calling this function both books will have the same union of
    highlights.  The raw_data dicts are updated and the ``.lua`` files are
    overwritten via :func:`~kohighlights.lua_codec.encode_file`.

    Raises:
        ValueError: if the books are not compatible (different title or
                    cre_dom_version).
    """
    if not same_book(book_a, book_b):
        raise ValueError(
            "Cannot merge books with different titles or cre_dom_version. "
            f"'{book_a.title}' vs '{book_b.title}'"
        )

    keys_a = {_highlight_key(h) for h in book_a.highlights}
    keys_b = {_highlight_key(h) for h in book_b.highlights}

    new_in_a = [h for h in book_b.highlights if _highlight_key(h) not in keys_a]
    new_in_b = [h for h in book_a.highlights if _highlight_key(h) not in keys_b]
    duplicates = len(book_a.highlights) + len(book_b.highlights) - len(new_in_a) - len(new_in_b)

    # Update in-memory model
    book_a.highlights = _dedup(book_a.highlights + new_in_a)
    book_b.highlights = _dedup(book_b.highlights + new_in_b)

    # Persist to .lua files
    result = MergeResult(added=len(new_in_a) + len(new_in_b), duplicates=duplicates)
    for book in (book_a, book_b):
        _write_back(book)
        result.saved_paths.append(book.path)

    return result


def sync_books(book_a: Book, book_b: Book) -> MergeResult:
    """Copy the furthest reading position to the other copy.

    Only ``percent_finished`` and the ``last_page`` in ``raw_data`` are
    synced; highlights are not touched.
    """
    if book_a.percent_finished >= book_b.percent_finished:
        leader, follower = book_a, book_b
    else:
        leader, follower = book_b, book_a

    follower.percent_finished = leader.percent_finished
    follower.raw_data["percent_finished"] = leader.percent_finished

    # Also copy last_page if present
    for key in ("last_page", "last_xpointer", "last_position"):
        if key in leader.raw_data:
            follower.raw_data[key] = leader.raw_data[key]

    _write_back(follower)
    return MergeResult(added=0, saved_paths=[follower.path])


# ── Write-back ────────────────────────────────────────────────────────────────


def _write_back(book: Book) -> None:
    """Serialise the book's raw_data (with updated highlights) back to disk."""
    raw = dict(book.raw_data)

    # Rebuild highlight structure from the in-memory list
    highs: dict = {}
    for h in book.highlights:
        page_key = h.page or 0
        if page_key not in highs:
            highs[page_key] = {}
        idx = len(highs[page_key])
        highs[page_key][idx] = {
            "text": h.text,
            "datetime": h.date,
            "chapter": h.chapter,
            "note": h.comment,
            "pageno": h.page_id,
        }
    raw["highlight"] = highs

    encode_file(book.path, raw)
