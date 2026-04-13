"""Shared domain models for KoHighlights.

All components import from here — never define domain types elsewhere.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ── Enumerations ────────────────────────────────────────────────────────────


class ViewMode(str, Enum):
    BOOKS = "books"
    HIGHLIGHTS = "highlights"


class SortField(str, Enum):
    TITLE = "title"
    AUTHOR = "author"
    TYPE = "type"
    PERCENT = "percent"
    RATING = "rating"
    HIGH_COUNT = "high_count"
    MODIFIED = "modified"
    PATH = "path"
    # highlight-table fields
    HIGHLIGHT = "highlight"
    COMMENT = "comment"
    DATE = "date"
    PAGE = "page"
    CHAPTER = "chapter"


class ExportFormat(str, Enum):
    TXT = "txt"
    HTML = "html"
    CSV = "csv"
    MARKDOWN = "md"
    JSON = "json"


class ExportMode(str, Enum):
    MANY = "many"   # one file per book
    ONE = "one"     # all books in a single file


class FilterType(str, Enum):
    ALL = "all"            # search in titles + highlights + comments
    HIGHLIGHTS = "highlights"
    COMMENTS = "comments"
    TITLES = "titles"


# ── Domain models ────────────────────────────────────────────────────────────


@dataclass
class Highlight:
    """A single highlighted passage from a book."""

    text: str
    page: int = 0
    date: str = ""
    chapter: str = ""
    comment: str = ""
    page_id: str = ""   # KOReader internal page identifier (for merging)

    def __post_init__(self) -> None:
        # Normalise None values that may come from Lua null
        self.text = self.text or ""
        self.chapter = self.chapter or ""
        self.comment = self.comment or ""
        self.date = self.date or ""
        self.page_id = self.page_id or ""


@dataclass
class Book:
    """Metadata and highlights for a single book."""

    path: str                                   # path to the .lua metadata file
    title: str = "NO TITLE FOUND"
    authors: str = "NO AUTHOR FOUND"
    series: str = ""
    language: str = ""
    pages: int = 0
    keywords: str = ""
    highlights: list[Highlight] = field(default_factory=list)
    rating: str = ""
    status: str = ""
    percent_finished: float = 0.0
    modified_date: str = ""
    cre_dom_version: str = ""                   # needed for highlight merging
    md5: str = ""                               # partial_md5_checksum from KOReader
    book_path: str = ""                         # actual book file path (may not exist)
    raw_data: dict = field(default_factory=dict)  # original Lua dict (for round-trip saves)

    @property
    def display_title(self) -> str:
        return self.title if self.title else "NO TITLE FOUND"

    @property
    def display_authors(self) -> str:
        return self.authors if self.authors else "NO AUTHOR FOUND"

    @property
    def highlight_count(self) -> int:
        return len(self.highlights)

    @property
    def percent_str(self) -> str:
        return f"{int(self.percent_finished * 100)}%" if self.percent_finished else ""

    @property
    def rating_str(self) -> str:
        return self.rating or ""

    def sort_key(self, field: SortField) -> str:
        mapping = {
            SortField.TITLE: self.display_title.lower(),
            SortField.AUTHOR: self.display_authors.lower(),
            SortField.PERCENT: self.percent_str,
            SortField.RATING: self.rating_str,
            SortField.HIGH_COUNT: str(self.highlight_count).zfill(6),
            SortField.MODIFIED: self.modified_date,
            SortField.PATH: self.path,
        }
        return mapping.get(field, "")


@dataclass
class ExportOptions:
    """Options controlling how highlights are exported."""

    format: ExportFormat = ExportFormat.TXT
    mode: ExportMode = ExportMode.MANY
    output_dir: str = ""
    show_page: bool = True
    show_date: bool = True
    show_chapter: bool = True
    show_comment: bool = True
    sort_by_page: bool = True           # False → sort by date


@dataclass
class FilterOptions:
    """Options controlling how books/highlights are filtered."""

    text: str = ""
    filter_type: FilterType = FilterType.ALL


@dataclass
class AppSettings:
    """Persisted application preferences."""

    last_dir: str = ""
    db_path: str = ""
    view_mode: ViewMode = ViewMode.BOOKS
    sort_col: SortField = SortField.MODIFIED
    sort_asc: bool = False
    window_width: int = 1200
    window_height: int = 750
    db_mode: bool = False                       # True → show Archived books
    show_exit_confirm: bool = True
    highlight_by_page: bool = True
    skip_version: str = "0.0.0.0"
    opened_times: int = 0
    toolbar_size: int = 48
