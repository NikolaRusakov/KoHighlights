"""Book info panel — shows metadata for the currently selected book."""

from __future__ import annotations

import flet as ft

from kohighlights.models import Book


class BookInfoPanel:
    """Collapsible panel below the books table showing detailed book metadata."""

    def __init__(self) -> None:
        self._title = self._field("Title")
        self._author = self._field("Author(s)")
        self._series = self._field("Series")
        self._language = self._field("Language", 100)
        self._pages = self._field("Pages", 80)
        self._tags = self._field("Tags")
        self._review = ft.TextField(
            label="Review",
            read_only=True,
            dense=True,
            multiline=True,
            max_lines=3,
            border_color=ft.Colors.TRANSPARENT,
            filled=True,
            visible=False,
        )
        self._body = ft.Column(
            [
                ft.Row([self._title, self._author], spacing=8),
                ft.Row([self._series, self._language, self._pages], spacing=8),
                self._tags,
                self._review,
            ],
            spacing=4,
        )
        self._toggle_icon = ft.Icon(ft.Icons.EXPAND_MORE, size=16)
        self._toggle_btn = ft.TextButton(
            content=ft.Row(
                [self._toggle_icon, ft.Text("Book Info", size=12)],
                spacing=4,
                tight=True,
            ),
            on_click=self._toggle,
        )
        self.control = ft.Column(
            [
                self._toggle_btn,
                ft.Container(
                    content=self._body,
                    padding=ft.Padding.symmetric(horizontal=8),
                ),
            ],
            spacing=2,
        )

    @staticmethod
    def _field(label: str, w: int | None = None) -> ft.TextField:
        tf = ft.TextField(
            label=label,
            read_only=True,
            dense=True,
            border_color=ft.Colors.TRANSPARENT,
            filled=True,
            expand=w is None,
        )
        if w:
            tf.width = w
        return tf

    def show(self, book: Book | None) -> None:
        if book is None:
            for f in (
                self._title,
                self._author,
                self._series,
                self._language,
                self._pages,
                self._tags,
            ):
                f.value = ""
            self._review.visible = False
        else:
            self._title.value = book.display_title
            self._author.value = book.display_authors
            self._series.value = book.series
            self._language.value = book.language
            self._pages.value = str(book.pages) if book.pages else ""
            self._tags.value = book.keywords
            review = (book.raw_data.get("summary") or {}).get("note", "")
            self._review.value = review
            self._review.visible = bool(review)
        self.control.update()

    def _toggle(self, e: ft.ControlEvent) -> None:
        self._body.visible = not self._body.visible
        self._toggle_icon.name = (
            ft.Icons.EXPAND_MORE if not self._body.visible else ft.Icons.EXPAND_LESS
        )
        self.control.update()
