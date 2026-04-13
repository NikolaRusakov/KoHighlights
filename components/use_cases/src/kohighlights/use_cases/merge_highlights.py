"""Use case: merge/sync highlights between two device copies of a book."""
from __future__ import annotations

from kohighlights.highlight_merger import merge_books, sync_books, MergeResult
from kohighlights.models import Book
from kohighlights.use_cases.manage_books import save_book


class MergeError(Exception):
    """Base error for merge/sync failures."""


class BookMismatchError(MergeError):
    """Raised when the two books are not the same content."""


class CREVersionMismatchError(MergeError):
    """Raised when the CRE engine versions differ (highlights incompatible)."""


def can_merge(book_a: Book, book_b: Book) -> bool:
    """Return True if the two books can have their highlights merged."""
    from kohighlights.highlight_merger.merger import same_book
    return same_book(book_a, book_b)


def merge_two_books(
    book_a: Book,
    book_b: Book,
    do_merge: bool = True,
    do_sync_position: bool = False,
    persist: bool = True,
) -> MergeResult:
    """Merge highlights and/or sync reading position for two copies of a book.

    Args:
        book_a, book_b: The two book copies (must be the same content).
        do_merge:        If True, merge highlights bidirectionally.
        do_sync_position: If True, also sync reading position (percent_finished).
        persist:         If True, write changes back to .lua files.

    Returns:
        :class:`~kohighlights.highlight_merger.MergeResult`

    Raises:
        BookMismatchError: if the books do not represent the same content.
        CREVersionMismatchError: if highlights are incompatible (different CRE).
    """
    from kohighlights.highlight_merger.merger import same_book
    if not same_book(book_a, book_b):
        raise BookMismatchError(
            f"These books appear to be different: '{book_a.title}' / '{book_b.title}'"
        )

    result = MergeResult()

    if do_merge:
        try:
            result = merge_books(book_a, book_b)
        except ValueError as exc:
            raise CREVersionMismatchError(str(exc)) from exc

    if do_sync_position:
        sync_result = sync_books(book_a, book_b)
        result.saved_paths.extend(sync_result.saved_paths)

    if persist and not do_merge:
        # merge_books already saves; only save if we skipped it
        save_book(book_a)
        save_book(book_b)

    return result
