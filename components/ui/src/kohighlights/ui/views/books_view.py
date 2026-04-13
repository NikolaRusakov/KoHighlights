"""Books table view — lists all loaded/archived books."""

from __future__ import annotations

from typing import Callable

import flet as ft

from kohighlights.models import Book
from kohighlights.ui.state import AppState


def _pct(p: float) -> str:
    return f"{int(p * 100)}%" if p else ""


class BooksView:
    """Scrollable sortable data table for the books list."""

    def __init__(
        self,
        state: AppState,
        on_selection_change: Callable[[list[Book]], None],
        on_open_book: Callable[[Book], None],
    ) -> None:
        self._state = state
        self._on_selection = on_selection_change
        self._on_open = on_open_book
        self._selected: set[str] = set()
        self._sort_col = 6
        self._sort_asc = False

        self._table = ft.DataTable(
            columns=self._make_columns(),
            rows=[],
            show_checkbox_column=True,
            sort_column_index=self._sort_col,
            sort_ascending=self._sort_asc,
            column_spacing=12,
            # on_sort=self._on_sort,
            horizontal_margin=8,
            data_row_min_height=28,
            data_row_max_height=40,
        )
        self.control = ft.Column(
            [ft.Row([self._table], scroll=ft.ScrollMode.AUTO)],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _make_columns(self) -> list[ft.DataColumn]:
        labels = [
            "Title",
            "Author",
            "Type",
            "%",
            "Rating",
            "Highlights",
            "Modified",
            "Path",
        ]
        return [
            ft.DataColumn(
                ft.Text(lbl, weight=ft.FontWeight.BOLD, size=12), on_sort=None
            )
            for lbl in labels
        ]

    def refresh(self, books: list[Book]) -> None:
        self._table.rows = [self._make_row(b) for b in books]
        self._table.update()

    def clear_selection(self) -> None:
        self._selected.clear()
        self._state.selected_books = []

    def _make_row(self, book: Book) -> ft.DataRow:
        is_sel = book.path in self._selected
        color = ft.Colors.RED_900 if book.status == "abandoned" else None

        def _c(txt: str, tip: str = "") -> ft.DataCell:
            return ft.DataCell(ft.Text(txt, color=color, size=12, tooltip=tip or None))

        book_path = getattr(book, "book_path", "") or ""
        ext = book_path.rsplit(".", 1)[-1] if "." in book_path else ""

        return ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Text(
                        book.display_title,
                        color=color,
                        size=12,
                        tooltip=book.display_title,
                    ),
                    on_double_tap=lambda e, b=book: self._on_open(b),
                ),
                _c(book.display_authors, book.display_authors),
                _c(ext, book_path),
                _c(_pct(book.percent_finished)),
                _c(book.rating_str),
                _c(str(book.highlight_count) if book.highlight_count else ""),
                _c(book.modified_date),
                _c(book.path, book.path),
            ],
            selected=is_sel,
            on_select_change=lambda e, b=book: self._toggle(e, b),
        )

    def _toggle(self, e: ft.ControlEvent, book: Book) -> None:
        if e.data == "true":
            self._selected.add(book.path)
        else:
            self._selected.discard(book.path)
        self._state.selected_books = [
            b for b in self._state.books if b.path in self._selected
        ]
        self._on_selection(self._state.selected_books)
        self._table.update()

    def _on_sort(self, e: ft.DataColumnSortEvent) -> None:
        self._sort_col = e.column_index
        self._sort_asc = e.ascending
        self._table.sort_column_index = self._sort_col
        self._table.sort_ascending = self._sort_asc

        key_fns = [
            lambda b: b.display_title.lower(),
            lambda b: b.display_authors.lower(),
            lambda b: (getattr(b, "book_path", "") or "").rsplit(".", 1)[-1],
            lambda b: b.percent_finished,
            lambda b: b.rating_str,
            lambda b: b.highlight_count,
            lambda b: b.modified_date,
            lambda b: b.path,
        ]
        self._state.displayed_books.sort(
            key=key_fns[self._sort_col], reverse=not self._sort_asc
        )
        self.refresh(self._state.displayed_books)
