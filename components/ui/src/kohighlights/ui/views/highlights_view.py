"""Highlights table view — all highlights across selected/loaded books."""

from __future__ import annotations

from typing import Callable

import flet as ft

from kohighlights.models import Highlight
from kohighlights.ui.state import AppState


class HighlightsView:
    """Full-page table of all highlights, used in Highlights view mode."""

    def __init__(
        self,
        state: AppState,
        on_selection_change: Callable[[list[Highlight]], None],
        on_edit_comment: Callable[[Highlight], None],
        on_copy: Callable[[Highlight], None],
        on_delete: Callable[[Highlight], None],
    ) -> None:
        self._state = state
        self._on_selection = on_selection_change
        self._on_edit = on_edit_comment
        self._on_copy = on_copy
        self._on_delete = on_delete
        self._highlights: list[Highlight] = []

        self._table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Highlight", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Comment", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Date", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Title", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Author", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Page", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Chapter", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            column_spacing=12,
            horizontal_margin=8,
            data_row_min_height=32,
            # on_sort=self._on_sort,
            sort_column_index=2,
            sort_ascending=False,
        )
        self.control = ft.Column(
            [ft.Row([self._table], scroll=ft.ScrollMode.AUTO)],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def refresh(self, highlights: list[Highlight]) -> None:
        self._highlights = highlights
        self._table.rows = [self._make_row(i, h) for i, h in enumerate(highlights)]
        self._table.update()

    def _make_row(self, idx: int, h: Highlight) -> ft.DataRow:
        def _c(txt: str, tip: str = "") -> ft.DataCell:
            return ft.DataCell(ft.Text(txt, size=12, tooltip=tip or None))

        return ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Text(
                        h.text[:100] + ("…" if len(h.text) > 100 else ""),
                        size=12,
                        selectable=True,
                    ),
                    on_tap=lambda e, hi=h: self._on_selection([hi]),
                    on_double_tap=lambda e, hi=h: self._on_edit(hi),
                ),
                _c(h.comment[:80] + ("…" if len(h.comment) > 80 else ""), h.comment),
                _c(h.date),
                _c(getattr(h, "title", "")[:60]),
                _c(getattr(h, "authors", "")[:40]),
                _c(str(h.page) if h.page else ""),
                _c(h.chapter[:60] if h.chapter else ""),
            ],
            on_select_changed=lambda e, hi=h: self._on_selection([hi]),
        )

    def _on_sort(self, e: ft.DataColumnSortEvent) -> None:
        col, asc = e.column_index, e.ascending
        key_fns = [
            lambda h: h.text.lower(),
            lambda h: h.comment.lower(),
            lambda h: h.date,
            lambda h: getattr(h, "title", "").lower(),
            lambda h: getattr(h, "authors", "").lower(),
            lambda h: h.page,
            lambda h: h.chapter.lower(),
        ]
        self._highlights.sort(key=key_fns[col], reverse=not asc)
        self.refresh(self._highlights)
