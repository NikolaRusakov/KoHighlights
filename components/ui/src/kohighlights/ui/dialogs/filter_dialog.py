"""Inline filter bar."""

from __future__ import annotations

from typing import Callable

import flet as ft

from kohighlights.models import FilterOptions, FilterType


class FilterBar:
    """Collapsible filter bar shown below the toolbar."""

    _TYPE_MAP = {
        "ALL": FilterType.ALL,
        "HIGHLIGHTS": FilterType.HIGHLIGHTS,
        "COMMENTS": FilterType.COMMENTS,
        "TITLES": FilterType.TITLES,
    }

    def __init__(self, on_change: Callable[[FilterOptions], None]) -> None:
        self._on_change = on_change

        self._input = ft.TextField(
            hint_text="Filter…",
            expand=True,
            dense=True,
            on_change=self._emit,
            on_submit=self._emit,
            prefix_icon=ft.Icons.SEARCH,
            border_radius=20,
        )
        self._type_dd = ft.Dropdown(
            width=190,
            dense=True,
            border_radius=20,
            options=[
                ft.dropdown.Option(key="ALL", text="All"),
                ft.dropdown.Option(key="HIGHLIGHTS", text="Highlights"),
                ft.dropdown.Option(key="COMMENTS", text="Comments"),
                ft.dropdown.Option(key="TITLES", text="Book titles"),
            ],
            value="ALL",
            # on_change=self._emit,
        )
        self._count = ft.Text("", size=12, color=ft.Colors.GREY_600)
        self._row = ft.Container(
            content=ft.Row(
                [
                    self._input,
                    self._type_dd,
                    self._count,
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_size=16,
                        tooltip="Clear filter",
                        on_click=self._do_clear,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.Padding.symmetric(horizontal=12, vertical=4),
            bgcolor=ft.Colors.GREEN,
            visible=False,
        )
        self.control = self._row

    def toggle(self) -> None:
        self._row.visible = not self._row.visible
        if not self._row.visible:
            self._do_clear(None)
        self._row.update()

    def set_count(self, shown: int, total: int) -> None:
        self._count.value = f"{shown} / {total}"
        self._count.update()

    def _emit(self, e) -> None:
        self._on_change(
            FilterOptions(
                text=self._input.value or "",
                filter_type=self._TYPE_MAP.get(
                    self._type_dd.value or "ALL", FilterType.ALL
                ),
            )
        )

    def _do_clear(self, e) -> None:
        self._input.value = ""
        self._count.value = ""
        self._on_change(FilterOptions())
        self._row.update()
