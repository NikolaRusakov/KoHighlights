"""Export highlights to TXT, HTML, CSV, Markdown, and JSON.

Two public functions cover both export modes:

* :func:`export_book`         — one output file per book (``ExportMode.MANY``)
* :func:`export_books_merged` — all books in a single file (``ExportMode.ONE``)
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Sequence

from kohighlights.models import Book, ExportFormat, ExportOptions, Highlight


# ── Templates ────────────────────────────────────────────────────────────────

_HTML_HEAD = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    body { background-color: #fafafa; font-family: Georgia, serif; max-width: 860px; margin: 0 auto; padding: 2rem; }
    .book-block { border: 2px solid rgba(20,20,20,.4); padding: 20px 20px 5px; background: #cdcdcd; border-radius: 18px; margin-bottom: 2rem; }
    .high-block { border: 2px solid rgba(115,173,33,.5); padding: 16px; background: #ebebeb; border-radius: 14px; margin: .8rem 0; }
    .meta { display: flex; justify-content: space-between; font-size: .8rem; color: #555; border-bottom: 1px solid #bbb; margin-bottom: .5rem; }
    h2, h3 { margin: .2rem 0; text-align: center; }
    h4 { margin: .2rem 0; font-style: italic; }
    p  { margin: .3rem 0; }
  </style>
  <title>KoHighlights</title>
</head>
<body>
"""

_BOOK_BLOCK_HTML = """\
<div class="book-block">
  <h2>{title}</h2>
  <h3>{authors}</h3>
"""

_HIGH_BLOCK_HTML = """\
  <div class="high-block">
    <div class="meta"><span>{page}</span><span>{date}</span></div>
    {chapter}<p>{highlight}</p>{comment}
  </div>
"""

_CSV_HEAD = "Title\tAuthors\tPage\tDate\tChapter\tHighlight\tComment\n"


# ── Helpers ──────────────────────────────────────────────────────────────────


def _sanitize(name: str) -> str:
    return re.sub(r'[/:*?"<>|\\]', "_", name)


def _sort_key(h: Highlight, by_page: bool) -> tuple:
    if by_page:
        return (h.page, h.date)
    return (h.date, h.page)


def _fmt_page(h: Highlight, opts: ExportOptions) -> str:
    return f"p.{h.page}" if (opts.show_page and h.page) else ""


def _fmt_date(h: Highlight, opts: ExportOptions) -> str:
    return h.date if opts.show_date else ""


def _fmt_chapter(h: Highlight, opts: ExportOptions) -> str:
    return h.chapter if opts.show_chapter else ""


def _fmt_comment(h: Highlight, opts: ExportOptions) -> str:
    return h.comment if opts.show_comment else ""


def _csv_row(title: str, authors: str, h: Highlight) -> str:
    def _esc(v: str) -> str:
        v = str(v).replace('"', '""')
        return f'"{v}"' if ("\n" in v or '"' in v) else v
    cols = [title, authors, str(h.page), h.date, h.chapter, h.text, h.comment]
    return "\t".join(_esc(c) for c in cols)


# ── Per-book (MANY) export ───────────────────────────────────────────────────


def export_book(book: Book, opts: ExportOptions) -> Path:
    """Write *book*'s highlights to a single file in *opts.output_dir*.

    Returns the path of the created file.
    """
    nl = os.linesep
    out_dir = Path(opts.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    name = f"{book.display_authors} - {book.display_title}" if book.authors else book.display_title
    stem = _sanitize(name)
    fmt = opts.format

    sorted_highs = sorted(book.highlights, key=lambda h: _sort_key(h, opts.sort_by_page))

    if fmt == ExportFormat.TXT:
        ext, enc = ".txt", "utf-8"
        line = "-" * 80
        body = line + nl + name + nl + line + (nl * 2)
        for h in sorted_highs:
            pg = _fmt_page(h, opts)
            dt = _fmt_date(h, opts)
            ch = _fmt_chapter(h, opts)
            cm = _fmt_comment(h, opts)
            body += (f"{pg}  {dt}{nl}" if (pg or dt) else "")
            body += (f"[{ch}]{nl}" if ch else "")
            body += h.text + nl
            body += (cm + nl if cm else "")
            body += nl

    elif fmt == ExportFormat.HTML:
        ext, enc = ".html", "utf-8"
        body = _HTML_HEAD + _BOOK_BLOCK_HTML.format(title=book.display_title, authors=book.display_authors)
        for h in sorted_highs:
            chapter_html = f"<h4>{h.chapter}</h4>" if (_fmt_chapter(h, opts)) else ""
            comment_html = f"<p><em>{h.comment}</em></p>" if (_fmt_comment(h, opts) and h.comment) else ""
            body += _HIGH_BLOCK_HTML.format(
                page=_fmt_page(h, opts),
                date=_fmt_date(h, opts),
                chapter=chapter_html,
                highlight=h.text.replace("\n", "<br/>"),
                comment=comment_html,
            )
        body += "\n</div>\n</body>\n</html>"

    elif fmt == ExportFormat.CSV:
        ext, enc = ".csv", "utf-8-sig"
        body = _CSV_HEAD
        for h in sorted_highs:
            body += _csv_row(book.display_title, book.display_authors, h) + "\n"

    elif fmt == ExportFormat.MARKDOWN:
        ext, enc = ".md", "utf-8"
        body = f"\n---\n## {book.display_title}  \n##### {book.display_authors}  \n---\n"
        for h in sorted_highs:
            pg = _fmt_page(h, opts)
            dt = _fmt_date(h, opts)
            ch = _fmt_chapter(h, opts)
            cm = _fmt_comment(h, opts)
            entry = f"*{pg}  {dt}*  \n" if (pg or dt) else ""
            if ch:
                entry += f"***{ch}***  \n"
            entry += h.text.replace("\n", "  \n") + "  \n"
            if cm:
                entry += cm.replace("\n", "  \n") + "  \n"
            entry += "&nbsp;  \n\n"
            body += entry.replace("-", "\\-")

    elif fmt == ExportFormat.JSON:
        ext, enc = ".json", "utf-8"
        records = []
        for h in sorted_highs:
            records.append({
                "title": book.display_title,
                "authors": book.display_authors,
                "page": h.page,
                "date": h.date,
                "chapter": h.chapter,
                "text": h.text,
                "comment": h.comment,
            })
        body = json.dumps(records, ensure_ascii=False, indent=2)

    else:
        raise ValueError(f"Unknown export format: {fmt}")

    out_path = out_dir / (stem + ext)
    # Avoid clobbering "NO TITLE" files
    if "NO TITLE FOUND" in book.display_title:
        idx = 1
        while out_path.exists():
            out_path = out_dir / (f"{stem} [{idx:02d}]{ext}")
            idx += 1

    out_path.write_text(body, encoding=enc, newline="")
    return out_path


# ── Merged (ONE) export ──────────────────────────────────────────────────────


def export_books_merged(
    books: Sequence[Book],
    opts: ExportOptions,
    filename: str | None = None,
) -> Path:
    """Merge highlights from multiple *books* into a single output file.

    Returns the path of the created file.
    """
    nl = os.linesep
    out_dir = Path(opts.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fmt = opts.format

    stems = {ExportFormat.TXT: ".txt", ExportFormat.HTML: ".html",
             ExportFormat.CSV: ".csv", ExportFormat.MARKDOWN: ".md",
             ExportFormat.JSON: ".json"}
    ext = stems.get(fmt, ".txt")
    enc = "utf-8-sig" if fmt == ExportFormat.CSV else "utf-8"
    stem = _sanitize(filename or "KoHighlights_export")
    out_path = out_dir / (stem + ext)

    chunks: list[str] = []

    if fmt == ExportFormat.HTML:
        chunks.append(_HTML_HEAD)
    elif fmt == ExportFormat.CSV:
        chunks.append(_CSV_HEAD)
    elif fmt == ExportFormat.JSON:
        all_records: list[dict] = []

    for book in books:
        if not book.highlights:
            continue
        sorted_highs = sorted(book.highlights, key=lambda h: _sort_key(h, opts.sort_by_page))

        if fmt == ExportFormat.TXT:
            line = "-" * 80
            chunks.append(line + nl + book.display_title + nl + line + nl * 2)
            for h in sorted_highs:
                pg = _fmt_page(h, opts)
                dt = _fmt_date(h, opts)
                ch = _fmt_chapter(h, opts)
                cm = _fmt_comment(h, opts)
                chunks.append((f"{pg}  {dt}{nl}" if (pg or dt) else ""))
                chunks.append((f"[{ch}]{nl}" if ch else ""))
                chunks.append(h.text + nl)
                chunks.append((cm + nl if cm else ""))
                chunks.append(nl)

        elif fmt == ExportFormat.HTML:
            chunks.append(_BOOK_BLOCK_HTML.format(title=book.display_title, authors=book.display_authors))
            for h in sorted_highs:
                chapter_html = f"<h4>{h.chapter}</h4>" if (_fmt_chapter(h, opts)) else ""
                comment_html = f"<p><em>{h.comment}</em></p>" if (_fmt_comment(h, opts) and h.comment) else ""
                chunks.append(_HIGH_BLOCK_HTML.format(
                    page=_fmt_page(h, opts),
                    date=_fmt_date(h, opts),
                    chapter=chapter_html,
                    highlight=h.text.replace("\n", "<br/>"),
                    comment=comment_html,
                ))
            chunks.append("</div>\n")

        elif fmt == ExportFormat.CSV:
            for h in sorted_highs:
                chunks.append(_csv_row(book.display_title, book.display_authors, h) + "\n")

        elif fmt == ExportFormat.MARKDOWN:
            chunks.append(f"\n---\n## {book.display_title}  \n##### {book.display_authors}  \n---\n")
            for h in sorted_highs:
                pg = _fmt_page(h, opts)
                dt = _fmt_date(h, opts)
                ch = _fmt_chapter(h, opts)
                cm = _fmt_comment(h, opts)
                entry = f"*{pg}  {dt}*  \n" if (pg or dt) else ""
                if ch:
                    entry += f"***{ch}***  \n"
                entry += h.text.replace("\n", "  \n") + "  \n"
                if cm:
                    entry += cm.replace("\n", "  \n") + "  \n"
                entry += "&nbsp;  \n\n"
                chunks.append(entry.replace("-", "\\-"))

        elif fmt == ExportFormat.JSON:
            for h in sorted_highs:
                all_records.append({
                    "title": book.display_title,
                    "authors": book.display_authors,
                    "page": h.page,
                    "date": h.date,
                    "chapter": h.chapter,
                    "text": h.text,
                    "comment": h.comment,
                })

    if fmt == ExportFormat.HTML:
        chunks.append("</body>\n</html>")

    if fmt == ExportFormat.JSON:
        body = json.dumps(all_records, ensure_ascii=False, indent=2)
    else:
        body = "".join(chunks)

    out_path.write_text(body, encoding=enc, newline="")
    return out_path
