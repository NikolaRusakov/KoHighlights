"""Gzip-compressed JSON settings persistence.

Mirrors the behaviour of the original application, which serialised settings
to ``settings.json.gz`` in the platform settings directory.
"""
from __future__ import annotations

import dataclasses
import gzip
import json
import os
import sys
import time
import traceback
from pathlib import Path
from typing import Any

from kohighlights.models import AppSettings, ViewMode, SortField


APP_NAME = "KOHighlights"


def get_settings_dir() -> Path:
    """Return the platform-specific directory for application data.

    On Android/iOS this fallback should not be used — callers should pass
    the path from ``ft.StoragePaths.get_application_support_directory()``.
    """
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", Path.home())
        return Path(base) / APP_NAME
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / APP_NAME
    # Android: ANDROID_ROOT env var is set to /system
    if os.environ.get("ANDROID_ROOT"):
        raise RuntimeError(
            "On Android, pass settings_dir from StoragePaths.get_application_support_directory()"
        )
    # Linux / BSD / other POSIX
    xdg = os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".local" / "share"))
    return Path(xdg) / APP_NAME


class SettingsStore:
    """Load and save :class:`~kohighlights.models.AppSettings`."""

    def __init__(self, settings_dir: str | Path | None = None) -> None:
        self.dir = Path(settings_dir) if settings_dir else get_settings_dir()
        self.dir.mkdir(parents=True, exist_ok=True)
        self._file = self.dir / "settings.json.gz"

    # ── Paths ────────────────────────────────────────────────────────────

    @property
    def default_db_path(self) -> Path:
        return self.dir / "data.db"

    @property
    def error_log_path(self) -> Path:
        today = time.strftime("%Y-%m-%d")
        return self.dir / f"error_log_{today}.txt"

    # ── Persistence ──────────────────────────────────────────────────────

    def load(self) -> AppSettings:
        """Return saved settings, or defaults on first run / parse error."""
        try:
            with gzip.open(self._file, "rb") as fh:
                raw: dict = json.loads(fh.read().decode("utf-8"))
        except Exception:
            raw = {}

        settings = AppSettings()
        if not raw:
            settings.db_path = str(self.default_db_path)
            return settings

        # Map stored values back to typed fields
        for f in dataclasses.fields(settings):
            if f.name not in raw:
                continue
            val = raw[f.name]
            if f.type == "ViewMode":
                val = ViewMode(val)
            elif f.type == "SortField":
                val = SortField(val)
            setattr(settings, f.name, val)

        if not settings.db_path:
            settings.db_path = str(self.default_db_path)
        return settings

    def save(self, settings: AppSettings) -> None:
        """Persist *settings* to disk."""
        raw: dict[str, Any] = {}
        for f in dataclasses.fields(settings):
            val = getattr(settings, f.name)
            raw[f.name] = val.value if isinstance(val, (ViewMode, SortField)) else val
        with gzip.open(self._file, "wb") as fh:
            fh.write(json.dumps(raw, ensure_ascii=False).encode("utf-8"))

    # ── Error logging ────────────────────────────────────────────────────

    def log_exception(
        self,
        exc_type: type,
        exc_value: BaseException,
        exc_tb: Any,
    ) -> None:
        try:
            with open(self.error_log_path, "a", encoding="utf-8") as fh:
                fh.write(f"\nCrash@{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                traceback.print_exception(exc_type, exc_value, exc_tb, file=fh)
        except OSError:
            pass
