"""Use case: filter books and highlights."""
from __future__ import annotations

from kohighlights.models import Book, Highlight, FilterOptions, FilterType


def filter_books(books: list[Book], opts: FilterOptions) -> list[Book]:
    """Return the subset of *books* matching *opts*.

    For ``ALL``, ``HIGHLIGHTS``, and ``COMMENTS`` filter types a book matches
    if any of its highlights/comments match.  For ``TITLES`` only the title is
    checked.
    """
    if not opts.text:
        return books

    q = opts.text.lower()
    ft = opts.filter_type
    result: list[Book] = []

    for book in books:
        if ft == FilterType.TITLES:
            if q in book.display_title.lower():
                result.append(book)
            continue

        # Title match satisfies ALL
        if ft == FilterType.ALL and q in book.display_title.lower():
            result.append(book)
            continue

        matched = False
        for h in book.highlights:
            if ft in (FilterType.ALL, FilterType.HIGHLIGHTS):
                if q in h.text.lower():
                    matched = True
                    break
            if ft in (FilterType.ALL, FilterType.COMMENTS):
                if q in h.comment.lower():
                    matched = True
                    break

        if matched:
            result.append(book)

    return result


def filter_highlights(highlights: list[Highlight], opts: FilterOptions) -> list[Highlight]:
    """Return the subset of *highlights* matching *opts*."""
    if not opts.text:
        return highlights

    q = opts.text.lower()
    ft = opts.filter_type
    result: list[Highlight] = []

    for h in highlights:
        matched = False
        if ft in (FilterType.ALL, FilterType.HIGHLIGHTS) and q in h.text.lower():
            matched = True
        elif ft in (FilterType.ALL, FilterType.COMMENTS) and q in h.comment.lower():
            matched = True
        elif ft == FilterType.TITLES and q in h.chapter.lower():
            # Chapter as proxy for title in flat highlights view
            matched = True
        if matched:
            result.append(h)

    return result
