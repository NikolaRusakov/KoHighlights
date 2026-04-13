"""Use case: export highlights to files."""
from __future__ import annotations

from pathlib import Path

from kohighlights.highlight_exporter import export_book, export_books_merged
from kohighlights.models import Book, ExportOptions, ExportMode


def export_books(
    books: list[Book],
    opts: ExportOptions,
) -> tuple[int, int]:
    """Export highlights for all *books* using *opts*.

    Returns ``(saved_count, skipped_no_highlights)``.
    """
    saved = 0
    skipped = 0

    if opts.mode == ExportMode.MANY:
        for book in books:
            if not book.highlights:
                skipped += 1
                continue
            export_book(book, opts)
            saved += 1
    else:
        # ONE — single merged file
        books_with_highlights = [b for b in books if b.highlights]
        skipped = len(books) - len(books_with_highlights)
        if books_with_highlights:
            export_books_merged(books_with_highlights, opts)
            saved = len(books_with_highlights)

    return saved, skipped
