"""Filesystem scanner for KOReader ``.sdr`` metadata folders.

Usage::

    from kohighlights.file_scanner import scan_for_books

    for book in scan_for_books("/mnt/kobo", on_progress=print):
        print(book.title, book.highlight_count)

The scanner walks the given root directory looking for ``*.sdr`` folders that
contain a ``metadata.*.lua`` file, then decodes the Lua file into a
:class:`~kohighlights.models.Book`.
"""
from __future__ import annotations

import hashlib
import os
from datetime import datetime
from os.path import getmtime, isfile, join, splitext, basename
from pathlib import Path
from typing import Callable, Generator, Iterable

from kohighlights.lua_codec import decode_file
from kohighlights.models import Book, Highlight


# ── Helpers ──────────────────────────────────────────────────────────────────


def _md5_short(path: str) -> str:
    """Return the first 8 chars of the MD5 hash of the file path string."""
    return hashlib.md5(path.encode("utf-8")).hexdigest()[:8]


def get_book_path(meta_path: str, data: dict) -> str:
    """Derive the actual book file path from the ``.sdr`` metadata path.

    KOReader stores metadata in ``<bookfile>.sdr/metadata.<ext>.lua``.
    We reverse-engineer the original book path from that.
    """
    # meta_path: /path/to/Book Title.epub.sdr/metadata.epub.lua
    sdr_dir = os.path.dirname(meta_path)               # …/Book Title.epub.sdr
    parent_dir = os.path.dirname(sdr_dir)              # …/
    sdr_name = os.path.basename(sdr_dir)               # Book Title.epub.sdr
    if sdr_name.endswith(".sdr"):
        book_name = sdr_name[:-4]                      # Book Title.epub
        return join(parent_dir, book_name)

    # Fallback: try doc_path from metadata
    doc_path = data.get("doc_path", "")
    return doc_path if doc_path else ""


def _extract_highlights(raw: dict) -> list[Highlight]:
    """Convert the raw ``highlight`` Lua dict into a list of :class:`Highlight`."""
    raw_highs = raw.get("highlight", {})
    if not raw_highs:
        return []

    highlights: list[Highlight] = []

    # KOReader stores highlights as nested dicts: {page: {idx: {text, …}}}
    if isinstance(raw_highs, dict):
        for page_key, page_data in raw_highs.items():
            if not isinstance(page_data, dict):
                continue
            for _idx, h in page_data.items():
                if not isinstance(h, dict):
                    continue
                text = str(h.get("text", "")).strip()
                if not text:
                    continue
                # Find a comment if there is an associated note
                comment = ""
                bookmark_data = raw.get("bookmarks") or {}
                # Some versions store the comment alongside the highlight
                comment = str(h.get("note", "") or h.get("comment", "")).strip()

                highlights.append(Highlight(
                    text=text,
                    page=int(page_key) if str(page_key).isdigit() else 0,
                    date=str(h.get("datetime", "") or h.get("date", "")).strip(),
                    chapter=str(h.get("chapter", "")).strip(),
                    comment=comment,
                    page_id=str(h.get("pageno", "") or h.get("pos0", "")).strip(),
                ))
    elif isinstance(raw_highs, list):
        # Newer KOReader format: flat list
        for h in raw_highs:
            if not isinstance(h, dict):
                continue
            text = str(h.get("text", "")).strip()
            if not text:
                continue
            highlights.append(Highlight(
                text=text,
                page=int(h.get("page", 0) or 0),
                date=str(h.get("datetime", "") or h.get("date", "")).strip(),
                chapter=str(h.get("chapter", "")).strip(),
                comment=str(h.get("note", "") or h.get("comment", "")).strip(),
                page_id=str(h.get("pageno", "") or h.get("pos0", "")).strip(),
            ))

    return highlights


def _raw_to_book(meta_path: str, raw: dict) -> Book:
    """Convert a decoded Lua dict into a :class:`Book`."""
    stats = raw.get("stats", {}) or {}
    summary = raw.get("summary", {}) or {}

    title = (stats.get("title") or raw.get("title") or "").strip()
    authors = (stats.get("authors") or raw.get("authors") or "").strip()

    try:
        pct = float(raw.get("percent_finished", 0) or 0)
    except (ValueError, TypeError):
        pct = 0.0

    rating_num = summary.get("rating")
    rating = (str(rating_num) + "★") if rating_num else ""

    modified = str(datetime.fromtimestamp(getmtime(meta_path))).split(".")[0]

    return Book(
        path=meta_path,
        title=title or "NO TITLE FOUND",
        authors=authors or "NO AUTHOR FOUND",
        series=str(raw.get("series", "") or "").strip(),
        language=str(raw.get("language", "") or "").strip(),
        pages=int(stats.get("pages", 0) or raw.get("pages", 0) or 0),
        keywords=str(raw.get("keywords", "") or "").strip(),
        highlights=_extract_highlights(raw),
        rating=rating,
        status=str(summary.get("status", "") or "").strip(),
        percent_finished=pct,
        modified_date=modified,
        cre_dom_version=str(raw.get("cre_dom_version", "") or "").strip(),
        md5=str(raw.get("partial_md5_checksum", _md5_short(meta_path))),
        book_path=get_book_path(meta_path, raw),
        raw_data=raw,
    )


def _find_lua_files(root: str) -> Generator[str, None, None]:
    """Yield absolute paths to ``metadata.*.lua`` files under *root*."""
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        # KOReader places metadata inside *.sdr directories
        if dirpath.endswith(".sdr"):
            for fn in filenames:
                if fn.startswith("metadata.") and fn.endswith(".lua"):
                    yield join(dirpath, fn)
        # Prune hidden directories to speed up scans on large trees
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]


# ── Public API ───────────────────────────────────────────────────────────────


def scan_for_books(
    roots: str | Iterable[str],
    on_progress: Callable[[str], None] | None = None,
    skip_paths: set[str] | None = None,
) -> Generator[Book, None, None]:
    """Walk *roots* for KOReader metadata and yield :class:`Book` objects.

    Args:
        roots:       A single path or iterable of paths to scan.
        on_progress: Optional callback called with each ``meta_path`` found,
                     before it is decoded.  Useful for progress reporting.
        skip_paths:  Set of ``meta_path`` values to skip (already loaded).

    Yields:
        :class:`~kohighlights.models.Book` instances.
    """
    if isinstance(roots, str):
        roots = [roots]

    skip = skip_paths or set()

    for root in roots:
        root = str(root)
        if not os.path.exists(root):
            continue
        # Accept a direct path to a .lua file or a directory to scan
        if isfile(root) and root.endswith(".lua"):
            lua_files: Iterable[str] = [root]
        else:
            lua_files = _find_lua_files(root)

        for meta_path in lua_files:
            if meta_path in skip:
                continue
            if on_progress:
                on_progress(meta_path)
            raw = decode_file(meta_path)
            if not raw:
                continue
            try:
                yield _raw_to_book(meta_path, raw)
            except Exception:
                continue  # skip malformed entries silently


def scan_from_db_records(
    records: Iterable[tuple[str, str, str, dict]],
) -> Generator[Book, None, None]:
    """Convert archived DB records into :class:`Book` objects.

    Args:
        records: Iterable of (md5, path, date, data_dict) tuples as returned
                 by :meth:`~kohighlights.book_store.BookStore.all_records`.

    Yields:
        :class:`~kohighlights.models.Book` instances.
    """
    for md5, path, date, data in records:
        try:
            book = _raw_to_book(path, data)
            book.md5 = md5
            book.modified_date = date
            yield book
        except Exception:
            continue
