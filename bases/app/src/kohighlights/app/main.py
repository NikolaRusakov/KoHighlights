"""KOHighlights — Flet multiplatform application.

Composition root: wires all components together, sets up Flet page,
and defines all event handlers as closures.

Architecture: Polylith + Use-Case pattern.
  bases/app  →  use_cases  →  {models, book_store, file_scanner,
                                highlight_exporter, highlight_merger, lua_codec}
  bases/app  →  ui         →  {models, use_cases}
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
from pathlib import Path

import flet as ft
import flet_permission_handler as fph

from kohighlights.book_store import BookStore, SettingsStore
from kohighlights.file_scanner.scanner import scan_for_books
from kohighlights.models import (
    AppSettings,
    Book,
    ExportFormat,
    ExportMode,
    ExportOptions,
    FilterOptions,
    Highlight,
    ViewMode,
)
from kohighlights.ui.components.book_info import BookInfoPanel
from kohighlights.ui.components.highlights_panel import HighlightsPanel
from kohighlights.ui.components.toolbar import AppToolbar
from kohighlights.ui.dialogs.about_dialog import build_about_dialog
from kohighlights.ui.dialogs.comment_dialog import open_comment_dialog
from kohighlights.ui.dialogs.export_dialog import ExportDialog
from kohighlights.ui.dialogs.filter_dialog import FilterBar
from kohighlights.ui.state import AppState
from kohighlights.ui.views.books_view import BooksView
from kohighlights.ui.views.highlights_view import HighlightsView
from kohighlights.use_cases import (
    export_highlights,
    filter_highlights,
    manage_books,
    merge_highlights,
    scan_books,
)

APP_NAME = "KOHighlights"
APP_VERSION = "2.0.0"


async def main(page: ft.Page) -> None:  # noqa: C901
    """Build and run the KOHighlights Flet application."""

    # ── Bootstrap ────────────────────────────────────────────────────────
    # StoragePaths gives the correct writable path per platform:
    #   Android → /data/user/0/<pkg>/files/
    #   iOS     → <sandbox>/Library/Application Support/
    #   macOS   → ~/Library/Application Support/
    #   Linux   → ~/.local/share/
    #   Windows → %APPDATA%\
    storage_paths = ft.StoragePaths()
    data_dir = await storage_paths.get_application_support_directory()
    settings_store = SettingsStore(settings_dir=Path(data_dir) / APP_NAME)
    settings = settings_store.load()

    db_store = BookStore(settings.db_path or str(settings_store.default_db_path))
    state = AppState(page=page, settings=settings)
    state.view_mode = settings.view_mode
    state.db_mode = settings.db_mode

    # ── Page config ───────────────────────────────────────────────────────
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window.min_width = 800
    page.window.min_height = 500
    page.window.width = settings.window_width
    page.window.height = settings.window_height
    page.padding = 0
    page.spacing = 0

    # =========================================================================
    # Event handlers
    # =========================================================================

    async def _on_scan(e) -> None:
        path = await picker.get_directory_path(
            dialog_title="Select folder to scan for KOReader metadata",
            initial_directory=settings.last_dir or str(Path.home()),
        )
        print(f"Selected path: {path}")
        if not path:
            return
        settings.last_dir = path
        toolbar.set_scanning(True)
        _picker_result(path)

    def _picker_result(path: str | None) -> None:
        print(path)
        if not path:
            return
        settings.last_dir = path
        # _picker_result(e)
        toolbar.set_scanning(True)

        def _worker() -> None:
            def _found(book: Book) -> None:
                state.books.append(book)
                state.loaded_paths.add(book.path)
                state.displayed_books = list(state.books)
                if len(state.books) % 5 == 0:
                    books_view.refresh(state.displayed_books)
                    page.update()

            if os.path.isdir(path):

                scanned_books_gen = scan_for_books(path)
                for book in scanned_books_gen:
                    _found(book)
                # for root, dirs, files in os.walk(path):
                #     print(dirs, files)
                #     # Only process directories ending with .sdr
                #     if root.endswith(".sdr"):
                #         for file in files:
                #             if file.startswith("metadata") and file.endswith(".lua"):
                #                 lua_file_path = os.path.join(root, file)
                #                 try:
                #                     decode_file(lua_file_path)
                #                 except Exception as exc:
                #                     print(f"Error decoding {lua_file_path}: {exc}")

            books_view.refresh(state.displayed_books)
            toolbar.set_scanning(False)
            page.update()

        page.run_thread(_worker)
        # _worker()

    def _on_export(fmt: ExportFormat, mode: ExportMode) -> None:
        if not state.selected_books:
            _snack("Select at least one book first.")
            return
        export_dlg.open(fmt, mode)

    def _on_export_confirmed(opts: ExportOptions) -> None:
        saved, skipped = export_highlights.export_books(state.selected_books, opts)
        _snack(f"Exported {saved} book(s). Skipped {skipped} (no highlights).")

    def _on_merge(do_merge: bool, do_sync: bool) -> None:
        if len(state.selected_books) != 2:
            _snack("Select exactly 2 books to merge/sync.")
            return
        a, b = state.selected_books
        try:
            result = merge_highlights.merge_two_books(
                a,
                b,
                do_merge=do_merge,
                do_sync_position=do_sync,
                persist=not state.db_mode,
            )
            if state.db_mode:
                db_store.upsert(a.md5, a.path, a.modified_date, a.raw_data)
                db_store.upsert(b.md5, b.path, b.modified_date, b.raw_data)
            books_view.refresh(state.displayed_books)
            _snack(
                f"Done. Added {result.added} highlight(s), "
                f"{result.duplicates} duplicate(s)."
            )
        except merge_highlights.BookMismatchError as exc:
            _alert("Cannot merge", str(exc))
        except merge_highlights.CREVersionMismatchError as exc:
            _alert("Version mismatch", str(exc))

    def _on_delete(action: int) -> None:
        books = list(state.selected_books)
        if not books and action != 2:
            _snack("Select at least one book first.")
            return
        if action == 0:
            manage_books.delete_books_info(books)
        elif action == 1:
            manage_books.delete_books_and_files(books)
        elif action == 2:
            missing = manage_books.get_missing_books(state.books)
            manage_books.delete_books_info(missing)
            books = missing

        for b in books:
            state.loaded_paths.discard(b.path)
            if b in state.books:
                state.books.remove(b)
        state.selected_books = []
        state.displayed_books = list(state.books)
        books_view.refresh(state.displayed_books)
        toolbar.update_state()

    def _on_clear(e) -> None:
        state.books = []
        state.loaded_paths = set()
        state.selected_books = []
        state.displayed_books = []
        state.all_highlights = []
        state.displayed_highlights = []
        books_view.refresh([])
        highlights_panel.show([])
        highlights_view.refresh([])
        book_info.show(None)
        toolbar.update_state()
        page.update()

    def _on_filter_toggle(e) -> None:
        filter_bar.toggle()
        page.update()

    def _on_filter_change(opts: FilterOptions) -> None:
        state.apply_filter(opts, notify=False)
        books_view.refresh(state.displayed_books)
        filter_bar.set_count(len(state.displayed_books), len(state.books))
        if state.view_mode == ViewMode.HIGHLIGHTS:
            highlights_view.refresh(state.displayed_highlights)
        page.update()

    def _on_archive(e) -> None:
        if not state.selected_books:
            _snack("Select at least one book first.")
            return
        added, empty, old = manage_books.archive_books(state.selected_books, db_store)
        _snack(
            f"Archived {added} book(s). "
            f"Skipped {empty} (no highlights), {old} (old format)."
        )

    def _on_view_toggle(mode: ViewMode) -> None:
        state.view_mode = mode
        is_books = mode == ViewMode.BOOKS
        books_layout.visible = is_books
        highlights_layout.visible = not is_books
        if not is_books:
            all_highs = scan_books.get_all_highlights(state.books)
            state.all_highlights = all_highs
            state.displayed_highlights = list(all_highs)
            highlights_view.refresh(state.displayed_highlights)
        page.update()

    def _on_db_toggle(archived: bool) -> None:
        state.db_mode = archived
        settings.db_mode = archived
        if archived:
            _load_from_archive()
        else:
            paths = list(state.loaded_paths)
            state.books = []
            state.loaded_paths = set()
            state.displayed_books = []
            books_view.refresh([])
            toolbar.set_scanning(True)

            def _worker() -> None:
                def _found(book: Book) -> None:
                    state.books.append(book)
                    state.loaded_paths.add(book.path)
                    state.displayed_books = list(state.books)

                for path in paths:
                    scan_books.scan_directory(path, _found, state.loaded_paths)
                books_view.refresh(state.displayed_books)
                toolbar.set_scanning(False)
                page.update()

            threading.Thread(target=_worker, daemon=True).start()

    def _on_about(e) -> None:
        page.dialog = about_dlg
        about_dlg.open = True
        page.update()

    def _on_book_selection_changed(selected: list[Book]) -> None:
        state.selected_books = selected
        book = selected[-1] if selected else None
        book_info.show(book)
        if book:
            highs = scan_books.get_highlights_for_book(book)
            highlights_panel.show(highs)
        else:
            highlights_panel.show([])
        toolbar.update_state()
        page.update()

    def _on_open_book(book: Book) -> None:
        path = getattr(book, "book_path", "") or ""
        if not path or not os.path.isfile(path):
            _snack("Book file not found on disk.")
            return
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def _on_highlights_view_selection_changed(highs: list[Highlight]) -> None:
        state.selected_highlights = highs

    def _on_edit_comment(h: Highlight) -> None:
        def _save(hi: Highlight, text: str) -> None:
            book = _find_book(hi)
            if book:
                manage_books.update_highlight_comment(book, hi, text)
                if not state.db_mode:
                    manage_books.save_book(book)
                else:
                    db_store.upsert(
                        book.md5, book.path, book.modified_date, book.raw_data
                    )
                if state.selected_books and book in state.selected_books:
                    highlights_panel.show(scan_books.get_highlights_for_book(book))

        open_comment_dialog(page, h, _save)

    def _on_copy_highlight(h: Highlight) -> None:
        page.set_clipboard(h.text)
        _snack("Copied to clipboard.")

    def _on_delete_highlight(h: Highlight) -> None:
        book = _find_book(h)
        if not book:
            return
        manage_books.delete_highlight(book, h)
        if not state.db_mode:
            manage_books.save_book(book)
        else:
            db_store.upsert(book.md5, book.path, book.modified_date, book.raw_data)
        if state.selected_books and book in state.selected_books:
            highlights_panel.show(scan_books.get_highlights_for_book(book))
        books_view.refresh(state.displayed_books)
        page.update()

    def _on_keyboard(e: ft.KeyboardEvent) -> None:
        ctrl = e.ctrl
        key = e.key
        if ctrl:
            if key == "l" or key == "L":
                _on_scan(None)
            elif key == "s" or key == "S":
                if state.selected_books:
                    _on_export(ExportFormat.TXT, ExportMode.MANY)
            elif key == "i" or key == "I":
                _on_about(None)
            elif key == "f" or key == "F":
                _on_filter_toggle(None)
            elif key == "Backspace":
                _on_clear(None)

    def _on_window_event(e: ft.WindowEvent) -> None:
        if e.data == "close":
            _shutdown()

    def _load_from_archive() -> None:
        toolbar.set_scanning(True)

        def _worker() -> None:
            books = scan_books.load_from_archive(db_store)
            state.books = books
            state.displayed_books = list(books)
            books_view.refresh(state.displayed_books)
            toolbar.set_scanning(False)
            page.update()

        threading.Thread(target=_worker, daemon=True).start()

    def _find_book(h: Highlight) -> Book | None:
        for b in state.books:
            if any(hi.text == h.text for hi in b.highlights):
                return b
        return None

    def _snack(message: str) -> None:
        page.show_dialog(ft.SnackBar(ft.Text(message), open=True))

    def _alert(title: str, body: str) -> None:
        def _close(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text(title, weight=ft.FontWeight.BOLD),
            content=ft.Text(body),
            actions=[ft.TextButton("OK", on_click=_close)],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def _shutdown() -> None:
        settings.window_width = int(page.window.width or 1200)
        settings.window_height = int(page.window.height or 750)
        settings.view_mode = state.view_mode
        settings.db_mode = state.db_mode
        settings_store.save(settings)
        db_store.close()

    # ── UI construction ───────────────────────────────────────────────────
    picker = ft.FilePicker(on_upload=_picker_result)

    if hasattr(page, "services"):
        page.services.append(picker)
    else:
        page.overlay.append(picker)
    about_dlg = build_about_dialog(page)
    filter_bar = FilterBar(on_change=_on_filter_change)
    export_dlg = ExportDialog(page, on_confirm=_on_export_confirmed)
    book_info = BookInfoPanel()
    highlights_panel = HighlightsPanel(
        on_edit_comment=_on_edit_comment,
        on_copy=_on_copy_highlight,
        on_delete=_on_delete_highlight,
    )
    books_view = BooksView(
        state=state,
        on_selection_change=_on_book_selection_changed,
        on_open_book=_on_open_book,
    )
    highlights_view = HighlightsView(
        state=state,
        on_selection_change=_on_highlights_view_selection_changed,
        on_edit_comment=_on_edit_comment,
        on_copy=_on_copy_highlight,
        on_delete=_on_delete_highlight,
    )
    toolbar = AppToolbar(
        state=state,
        on_scan=_on_scan,
        on_export=_on_export,
        on_merge=_on_merge,
        on_delete=_on_delete,
        on_clear=_on_clear,
        on_filter_toggle=_on_filter_toggle,
        on_archive=_on_archive,
        on_about=_on_about,
        on_view_toggle=_on_view_toggle,
        on_db_toggle=_on_db_toggle,
    )

    # ── Layout ────────────────────────────────────────────────────────────
    books_left = ft.Column(
        [
            ft.Container(books_view.control, expand=True),
            ft.Divider(height=1),
            book_info.control,
        ],
        expand=True,
        spacing=0,
    )

    books_layout = ft.Container(
        content=ft.Row(
            [
                ft.Container(books_left, expand=3),
                ft.VerticalDivider(width=1, thickness=1),
                ft.Container(highlights_panel.control, expand=2, padding=8),
            ],
            expand=True,
            spacing=0,
        ),
        expand=True,
        visible=(state.view_mode == ViewMode.BOOKS),
    )
    highlights_layout = ft.Container(
        content=highlights_view.control,
        expand=True,
        visible=(state.view_mode == ViewMode.HIGHLIGHTS),
    )

    page.add(
        toolbar.control,
        filter_bar.control,
        ft.Divider(height=1),
        ft.Container(
            content=ft.Stack([books_layout, highlights_layout]),
            expand=True,
            padding=ft.Padding.symmetric(horizontal=4),
        ),
    )

    # ── Initial data load ─────────────────────────────────────────────────
    if settings.db_mode:
        _load_from_archive()

    page.on_keyboard_event = _on_keyboard
    page.on_window_event = _on_window_event
    page.update()


# ── CLI entry point ───────────────────────────────────────────────────────────


def run() -> None:
    """Start the application."""
    ft.run(main)


if __name__ == "__main__":
    run()
