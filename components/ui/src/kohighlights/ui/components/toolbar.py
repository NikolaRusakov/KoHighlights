"""Application toolbar built with Flet."""
from __future__ import annotations

from functools import partial
from typing import Callable

import flet as ft

from kohighlights.models import ExportFormat, ExportMode, ViewMode
from kohighlights.ui.state import AppState


class AppToolbar:
    """Main toolbar.  All action callbacks are injected via constructor."""

    def __init__(
        self,
        state: AppState,
        on_scan: Callable,
        on_export: Callable[[ExportFormat, ExportMode], None],
        on_merge: Callable[[bool, bool], None],
        on_delete: Callable[[int], None],
        on_clear: Callable,
        on_filter_toggle: Callable,
        on_archive: Callable,
        on_about: Callable,
        on_view_toggle: Callable[[ViewMode], None],
        on_db_toggle: Callable[[bool], None],
    ) -> None:
        self._state = state
        self._on_scan = on_scan
        self._on_export = on_export
        self._on_merge = on_merge
        self._on_delete = on_delete
        self._on_clear = on_clear
        self._on_filter_toggle = on_filter_toggle
        self._on_archive = on_archive
        self._on_about = on_about
        self._on_view_toggle = on_view_toggle
        self._on_db_toggle = on_db_toggle

        self._scan_btn = ft.IconButton(
            icon=ft.icons.FOLDER_OPEN_OUTLINED,
            tooltip="Scan directory (Ctrl+L)",
            on_click=on_scan,
        )
        self._export_btn = ft.PopupMenuButton(
            icon=ft.icons.SAVE_ALT_OUTLINED,
            tooltip="Export highlights",
            items=self._export_items(),
            disabled=True,
        )
        self._merge_btn = ft.PopupMenuButton(
            icon=ft.icons.MERGE_OUTLINED,
            tooltip="Merge / sync (select 2 books)",
            items=[
                ft.PopupMenuItem(
                    text="Merge highlights",
                    on_click=lambda e: on_merge(True, False),
                ),
                ft.PopupMenuItem(
                    text="Sync reading position",
                    on_click=lambda e: on_merge(False, True),
                ),
                ft.PopupMenuDivider(),
                ft.PopupMenuItem(
                    text="Merge highlights + sync position",
                    on_click=lambda e: on_merge(True, True),
                ),
            ],
            disabled=True,
        )
        self._delete_btn = ft.PopupMenuButton(
            icon=ft.icons.DELETE_OUTLINE,
            tooltip="Delete",
            items=[
                ft.PopupMenuItem(
                    text="Delete selected books' info",
                    on_click=lambda e: on_delete(0),
                ),
                ft.PopupMenuItem(
                    text="Delete selected book files + info",
                    on_click=lambda e: on_delete(1),
                ),
                ft.PopupMenuDivider(),
                ft.PopupMenuItem(
                    text="Delete all missing books' info",
                    on_click=lambda e: on_delete(2),
                ),
            ],
            disabled=True,
        )
        self._archive_btn = ft.IconButton(
            icon=ft.icons.ARCHIVE_OUTLINED,
            tooltip="Archive selected books to DB",
            on_click=lambda e: on_archive(e),
            disabled=True,
        )
        self._clear_btn = ft.IconButton(
            icon=ft.icons.CLEAR_ALL,
            tooltip="Clear list (Ctrl+Backspace)",
            on_click=on_clear,
        )
        self._filter_btn = ft.IconButton(
            icon=ft.icons.FILTER_ALT_OUTLINED,
            tooltip="Toggle filter (Ctrl+F)",
            on_click=on_filter_toggle,
        )
        self._view_seg = ft.SegmentedButton(
            selected={"books"},
            allow_empty_selection=False,
            allow_multiple_selection=False,
            segments=[
                ft.Segment(
                    value="books",
                    icon=ft.Icon(ft.icons.MENU_BOOK_OUTLINED),
                    label=ft.Text("Books"),
                ),
                ft.Segment(
                    value="highlights",
                    icon=ft.Icon(ft.icons.FORMAT_QUOTE_OUTLINED),
                    label=ft.Text("Highlights"),
                ),
            ],
            on_change=self._view_changed,
        )
        self._db_seg = ft.SegmentedButton(
            selected={"loaded"},
            allow_empty_selection=False,
            allow_multiple_selection=False,
            segments=[
                ft.Segment(value="loaded",   label=ft.Text("Loaded")),
                ft.Segment(
                    value="archived",
                    label=ft.Text("Archived"),
                    icon=ft.Icon(ft.icons.STORAGE_OUTLINED),
                ),
            ],
            on_change=self._db_mode_changed,
        )
        self._about_btn = ft.IconButton(
            icon=ft.icons.INFO_OUTLINE,
            tooltip="About (Ctrl+I)",
            on_click=lambda e: on_about(e),
        )
        self._spinner = ft.ProgressRing(
            width=18, height=18, stroke_width=2, visible=False
        )

        self.control = ft.Container(
            content=ft.Row(
                [
                    self._scan_btn,
                    ft.VerticalDivider(width=1, thickness=1),
                    self._export_btn,
                    self._merge_btn,
                    self._delete_btn,
                    self._archive_btn,
                    self._clear_btn,
                    ft.VerticalDivider(width=1, thickness=1),
                    self._filter_btn,
                    ft.VerticalDivider(width=1, thickness=1),
                    self._db_seg,
                    self._view_seg,
                    ft.VerticalDivider(width=1, thickness=1),
                    self._about_btn,
                    ft.Container(expand=True),
                    self._spinner,
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

    def update_state(self) -> None:
        sel = self._state.selected_books
        self._export_btn.disabled = not sel
        self._delete_btn.disabled = not sel
        self._archive_btn.disabled = not sel
        self._merge_btn.disabled = len(sel) != 2
        self.control.update()

    def set_scanning(self, scanning: bool) -> None:
        self._state.is_scanning = scanning
        self._spinner.visible = scanning
        self._scan_btn.disabled = scanning
        self.control.update()

    def _view_changed(self, e: ft.ControlEvent) -> None:
        val = list(e.data)[0]
        self._on_view_toggle(
            ViewMode.BOOKS if val == "books" else ViewMode.HIGHLIGHTS
        )

    def _db_mode_changed(self, e: ft.ControlEvent) -> None:
        val = list(e.data)[0]
        self._on_db_toggle(val == "archived")

    def _export_items(self) -> list[ft.PopupMenuItem]:
        groups: list[tuple[str, ExportFormat, ExportMode]] = [
            ("Individual TXT files",      ExportFormat.TXT,      ExportMode.MANY),
            ("Combined TXT file",         ExportFormat.TXT,      ExportMode.ONE),
            ("Individual HTML files",     ExportFormat.HTML,     ExportMode.MANY),
            ("Combined HTML file",        ExportFormat.HTML,     ExportMode.ONE),
            ("Individual CSV files",      ExportFormat.CSV,      ExportMode.MANY),
            ("Combined CSV file",         ExportFormat.CSV,      ExportMode.ONE),
            ("Individual Markdown files", ExportFormat.MARKDOWN, ExportMode.MANY),
            ("Combined Markdown file",    ExportFormat.MARKDOWN, ExportMode.ONE),
            ("Combined JSON file",        ExportFormat.JSON,     ExportMode.ONE),
        ]
        items: list[ft.PopupMenuItem] = []
        last_fmt: ExportFormat | None = None
        for label, fmt, mode in groups:
            if last_fmt and last_fmt != fmt:
                items.append(ft.PopupMenuDivider())
            items.append(ft.PopupMenuItem(
                text=label,
                on_click=partial(self._export_clicked, fmt, mode),
            ))
            last_fmt = fmt
        return items

    def _export_clicked(
        self, fmt: ExportFormat, mode: ExportMode, e: ft.ControlEvent
    ) -> None:
        self._on_export(fmt, mode)
