"""Export destination picker."""

from __future__ import annotations

from typing import Callable

import flet as ft

from kohighlights.models import ExportFormat, ExportMode, ExportOptions


class ExportDialog:
    """Wraps a FilePicker for selecting export destination."""

    def __init__(
        self, page: ft.Page, on_confirm: Callable[[ExportOptions], None]
    ) -> None:
        self._page = page
        self._on_confirm = on_confirm
        self._fmt: ExportFormat | None = None
        self._mode: ExportMode | None = None

        # self._picker = ft.FilePicker(
        #     on_upload=self._on_result,
        # )
        # page.overlay.append(self._picker)

        picker = ft.FilePicker(on_upload=self._on_result)
        if hasattr(page, "services"):
            page.services.append(picker)
        else:
            page.overlay.append(picker)

    def open(self, fmt: ExportFormat, mode: ExportMode) -> None:
        self._fmt = fmt
        self._mode = mode

        if mode == ExportMode.MANY:
            self._picker.get_directory_path(dialog_title="Select export folder")
        else:
            ext_map = {
                ExportFormat.TXT: "txt",
                ExportFormat.HTML: "html",
                ExportFormat.CSV: "csv",
                ExportFormat.MARKDOWN: "md",
                ExportFormat.JSON: "json",
            }
            ext = ext_map.get(fmt, "txt")
            self._picker.save_file(
                dialog_title=f"Save {ext.upper()} export",
                allowed_extensions=[ext],
                file_name=f"KoHighlights_export.{ext}",
            )
        self._page.update()

    def _on_result(self, e: ft.FilePickerResultEvent) -> None:
        path = e.path
        if not path and e.files:
            path = e.files[0].path
        if not path:
            return
        if self._fmt is not None and self._mode is not None:
            self._on_confirm(
                ExportOptions(
                    format=self._fmt,
                    mode=self._mode,
                    output_dir=path,
                )
            )
