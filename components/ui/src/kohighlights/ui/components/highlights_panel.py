"""Highlights side-panel shown in Books view."""

from __future__ import annotations

from typing import Callable

import flet as ft

from kohighlights.models import Highlight


class HighlightsPanel:
    """Scrollable list of highlights for the currently selected book(s)."""

    def __init__(
        self,
        on_edit_comment: Callable[[Highlight], None],
        on_copy: Callable[[Highlight], None],
        on_delete: Callable[[Highlight], None],
    ) -> None:
        self._on_edit = on_edit_comment
        self._on_copy = on_copy
        self._on_delete = on_delete

        self._count_lbl = ft.Text("", size=12, color=ft.Colors.GREY_600)
        self._list = ft.ListView(controls=[], spacing=6, padding=8, expand=True)
        self.control = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Highlights", weight=ft.FontWeight.BOLD, size=13),
                        self._count_lbl,
                    ],
                    spacing=6,
                ),
                ft.Divider(height=2),
                self._list,
            ],
            expand=True,
            spacing=4,
        )

    def show(self, highlights: list[Highlight]) -> None:
        self._count_lbl.value = f"({len(highlights)})" if highlights else ""
        self._list.controls = [self._make_card(h) for h in highlights]
        self.control.update()

    def _make_card(self, h: Highlight) -> ft.Control:
        meta = "  ·  ".join(p for p in [f"p.{h.page}" if h.page else "", h.date] if p)
        actions = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.EDIT_OUTLINED,
                    icon_size=15,
                    tooltip="Edit comment",
                    on_click=lambda e, hi=h: self._on_edit(hi),
                ),
                ft.IconButton(
                    icon=ft.Icons.COPY_OUTLINED,
                    icon_size=15,
                    tooltip="Copy text",
                    on_click=lambda e, hi=h: self._on_copy(hi),
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINED,
                    icon_size=15,
                    tooltip="Delete highlight",
                    on_click=lambda e, hi=h: self._on_delete(hi),
                ),
            ],
            spacing=0,
            visible=False,
        )

        inner = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(meta, size=11, color=ft.Colors.GREY_500),
                        ft.Container(expand=True),
                        actions,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                *(
                    [
                        ft.Text(
                            f"[{h.chapter}]",
                            size=11,
                            italic=True,
                            color=ft.Colors.BLUE_GREY_400,
                        )
                    ]
                    if h.chapter
                    else []
                ),
                ft.Text(h.text, selectable=True, size=13),
                *(
                    [
                        ft.Text(
                            f"● {h.comment}",
                            size=12,
                            italic=True,
                            color=ft.Colors.GREEN_700,
                            selectable=True,
                        )
                    ]
                    if h.comment
                    else []
                ),
            ],
            spacing=4,
        )

        card = ft.Container(
            content=inner,
            padding=10,
            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=10,
        )
        # Show/hide action buttons on hover
        card.on_hover = lambda e, ac=actions, c=card: (
            setattr(ac, "visible", e.data == "true") or c.update()
        )
        return card
