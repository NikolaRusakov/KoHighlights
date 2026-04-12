"""Comment editor dialog."""
from __future__ import annotations

from typing import Callable

import flet as ft

from kohighlights.models import Highlight


def open_comment_dialog(
    page: ft.Page,
    highlight: Highlight,
    on_save: Callable[[Highlight, str], None],
) -> None:
    """Open a dialog to edit the comment for *highlight*."""

    field = ft.TextField(
        value=highlight.comment,
        multiline=True,
        min_lines=3,
        max_lines=8,
        expand=True,
        label="Comment",
    )

    def _save(e: ft.ControlEvent) -> None:
        on_save(highlight, field.value or "")
        dlg.open = False
        page.update()

    def _cancel(e: ft.ControlEvent) -> None:
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Edit Comment"),
        content=ft.Column(
            [
                ft.Text(
                    highlight.text[:200] + ("…" if len(highlight.text) > 200 else ""),
                    size=12,
                    color=ft.colors.GREY_600,
                    italic=True,
                ),
                ft.Divider(),
                field,
            ],
            tight=True,
            spacing=8,
            width=500,
        ),
        actions=[
            ft.TextButton("Cancel", on_click=_cancel),
            ft.FilledButton("Save", on_click=_save),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.dialog = dlg
    dlg.open = True
    page.update()
