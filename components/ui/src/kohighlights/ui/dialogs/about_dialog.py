"""About / info dialog."""
from __future__ import annotations

import webbrowser

import flet as ft

APP_NAME = "KOHighlights"
APP_VERSION = "2.0.0"
_GITHUB_URL = "https://github.com/noEmbryo/KoHighlights"


def build_about_dialog(page: ft.Page) -> ft.AlertDialog:
    """Create and return the About dialog (not opened yet)."""

    def _close(e: ft.ControlEvent) -> None:
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text(f"About {APP_NAME}", weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                ft.Text(
                    f"{APP_NAME}  v{APP_VERSION}",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.PRIMARY,
                ),
                ft.Text("View and export your KOReader book highlights."),
                ft.Divider(),
                ft.Row([
                    ft.TextButton(
                        "GitHub",
                        icon=ft.icons.CODE,
                        on_click=lambda e: webbrowser.open(_GITHUB_URL),
                    ),
                ]),
                ft.Text(
                    "Built with Flet · Polylith · Python",
                    size=11,
                    color=ft.colors.GREY_600,
                    italic=True,
                ),
            ],
            tight=True,
            spacing=8,
        ),
        actions=[ft.TextButton("Close", on_click=_close)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return dlg
