"""Centralised reactive application state.

The ``AppState`` dataclass is the single source of truth for the running
application.  All UI components hold a reference to it.  Mutation methods
call registered listeners so that the UI can re-render.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import flet as ft

from kohighlights.models import (
    AppSettings,
    Book,
    FilterOptions,
    Highlight,
    ViewMode,
)


@dataclass
class AppState:
    """Central reactive state.  UI components subscribe with :meth:`subscribe`."""

    page: ft.Page
    settings: AppSettings

    # ── Data ─────────────────────────────────────────────────────────────
    books: list[Book] = field(default_factory=list)
    selected_books: list[Book] = field(default_factory=list)
    displayed_books: list[Book] = field(default_factory=list)  # post-filter

    all_highlights: list[Highlight] = field(default_factory=list)
    selected_highlights: list[Highlight] = field(default_factory=list)
    displayed_highlights: list[Highlight] = field(default_factory=list)

    # ── UI flags ──────────────────────────────────────────────────────────
    loaded_paths: set[str] = field(default_factory=set)
    view_mode: ViewMode = ViewMode.BOOKS
    db_mode: bool = False           # True = show archived books
    is_scanning: bool = False
    filter_opts: FilterOptions = field(default_factory=FilterOptions)
    status_message: str = ""

    # ── Listeners ─────────────────────────────────────────────────────────
    _listeners: list[Callable[[], None]] = field(default_factory=list, repr=False)

    def subscribe(self, fn: Callable[[], None]) -> None:
        self._listeners.append(fn)

    def notify(self, update_page: bool = True) -> None:
        for fn in self._listeners:
            fn()
        if update_page:
            self.page.update()

    # ── Convenience ───────────────────────────────────────────────────────

    def set_books(self, books: list[Book], *, notify: bool = True) -> None:
        self.books = books
        self.displayed_books = list(books)
        self.selected_books = []
        self.selected_highlights = []
        if notify:
            self.notify()

    def add_book(self, book: Book, *, notify: bool = True) -> None:
        self.books.append(book)
        self.loaded_paths.add(book.path)
        # Apply current filter to decide if it goes into displayed list
        from kohighlights.use_cases.filter_highlights import filter_books
        self.displayed_books = filter_books(self.books, self.filter_opts)
        if notify:
            self.notify()

    def apply_filter(self, opts: FilterOptions, *, notify: bool = True) -> None:
        from kohighlights.use_cases.filter_highlights import (
            filter_books,
            filter_highlights,
        )
        self.filter_opts = opts
        self.displayed_books = filter_books(self.books, opts)
        self.displayed_highlights = filter_highlights(self.all_highlights, opts)
        if notify:
            self.notify()
