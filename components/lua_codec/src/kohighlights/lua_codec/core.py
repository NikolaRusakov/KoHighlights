"""Lua ↔ Python codec for KOReader metadata files.

KOReader stores book metadata as Lua tables.  This module provides
``decode_file`` / ``encode_file`` as the public API.  The low-level
parser is a cleaned-up port of the original SLPPU library
(https://github.com/noembryo/slppu).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any


# ── Exceptions ───────────────────────────────────────────────────────────────


class LuaDecodeError(ValueError):
    """Raised when a Lua source file cannot be parsed."""


# ── Low-level parser ─────────────────────────────────────────────────────────


class _LuaParser:
    """Recursive-descent parser that converts Lua table literals to Python objects."""

    _WORDS = {"true": True, "false": False, "nil": None}
    _SPACE = re.compile(r"\s", re.MULTILINE)
    _ALNUM = re.compile(r"\w", re.MULTILINE)

    def __init__(self) -> None:
        self._text = ""
        self._ch: str | None = ""
        self._at = 0
        self._len = 0

    # ── Public entry point ───────────────────────────────────────────────

    def decode(self, text: str) -> Any:
        if not text or not isinstance(text, str):
            return None
        # Strip Lua line-comments
        text = re.sub(r"--.*$", "", text, flags=re.MULTILINE)
        self._text = text
        self._at = 0
        self._len = len(text)
        self._next()
        return self._value()

    def encode(self, obj: Any, depth: int = 0) -> str:
        tab = "    "
        nl = "\n"
        tp = type(obj)
        if tp is str:
            return '"%s"' % obj.replace('"', '\\"')
        if tp in (int, float):
            return str(obj)
        if tp is bool:
            return str(obj).lower()
        if obj is None:
            return "nil"
        if tp in (list, tuple, dict):
            depth += 1
            indent = tab * depth
            if tp is dict:
                items = []
                for k, v in obj.items():
                    key = (f"[{k}]" if isinstance(k, (int, float)) else f'["{k}"]')
                    items.append(f"{indent}{key} = {self.encode(v, depth)}")
                body = (",\n").join(items)
            else:
                items = [f"{indent}{self.encode(el, depth)}" for el in obj]
                body = (",\n").join(items)
            closing = tab * (depth - 1)
            return "{\n" + body + f"\n{closing}}}"
        return str(obj)

    # ── Internals ────────────────────────────────────────────────────────

    def _next(self) -> bool:
        if self._at >= self._len:
            self._ch = None
            return False
        self._ch = self._text[self._at]
        self._at += 1
        return True

    def _white(self) -> None:
        while self._ch and self._SPACE.match(self._ch):
            self._next()

    def _value(self) -> Any:
        self._white()
        if not self._ch:
            return None
        if self._ch == "{":
            return self._object()
        if self._ch == "[":
            self._next()
        if self._ch in ('"', "'", "["):
            return self._string(self._ch)
        if self._ch and (self._ch.isdigit() or self._ch == "-"):
            return self._number()
        return self._word()

    def _string(self, end: str) -> str:
        s = ""
        start = self._ch
        if end == "[":
            end = "]"
        if start in ('"', "'", "["):
            while self._next():
                if self._ch == end:
                    self._next()
                    if start != "[" or self._ch == "]":
                        return s
                if self._ch == "\\" and start == end:
                    self._next()
                    if self._ch != end:
                        s += "\\"
                s += self._ch
        return s  # unterminated string — return what we have

    def _object(self) -> dict | list:
        o: dict = {}
        k = None
        idx = 0
        numeric_keys = False
        self._next()
        self._white()
        if self._ch == "}":
            self._next()
            return o
        while self._ch:
            self._white()
            if self._ch == "{":
                o[idx] = self._object()
                idx += 1
                continue
            if self._ch == "}":
                self._next()
                if k is not None:
                    o[idx] = k
                if not numeric_keys and not any(
                    isinstance(key, (str, float, bool, tuple)) for key in o
                ):
                    arr: list = []
                    for key in o:
                        arr.insert(key, o[key])
                    return arr
                return o
            if self._ch == ",":
                self._next()
                continue
            k = self._value()
            if self._ch == "]":
                numeric_keys = True
                self._next()
            self._white()
            ch = self._ch
            if ch in ("=", ","):
                self._next()
                self._white()
                if ch == "=":
                    o[k] = self._value()
                else:
                    o[idx] = k
                idx += 1
                k = None
        return o  # unterminated table

    def _word(self) -> Any:
        s = ""
        if self._ch != "\n":
            s = self._ch
        self._next()
        while self._ch is not None and self._ALNUM.match(self._ch) and s not in self._WORDS:
            s += self._ch
            self._next()
        return self._WORDS.get(s, s)

    def _number(self) -> int | float:
        n = ""
        try:
            if self._ch == "-":
                n += self._ch
                self._next()
                if not self._ch or not self._ch.isdigit():
                    raise LuaDecodeError("Malformed number: no digits after minus")
            n += self._digits()
            if n.lstrip("-") == "0" and self._ch in ("x", "X"):
                n += self._ch
                self._next()
                n += self._hex_digits()
            else:
                if self._ch == ".":
                    n += self._ch
                    self._next()
                    if not self._ch or not self._ch.isdigit():
                        raise LuaDecodeError("Malformed number: no digits after decimal")
                    n += self._digits()
                if self._ch and self._ch in ("e", "E"):
                    n += self._ch
                    self._next()
                    if not self._ch or self._ch not in ("+", "-"):
                        raise LuaDecodeError("Malformed number: bad exponent")
                    n += self._ch
                    self._next()
                    n += self._digits()
        except LuaDecodeError:
            return 0
        try:
            return int(n, 0)
        except (ValueError, TypeError):
            return float(n)

    def _digits(self) -> str:
        s = ""
        while self._ch and self._ch.isdigit():
            s += self._ch
            self._next()
        return s

    def _hex_digits(self) -> str:
        s = ""
        while self._ch and (self._ch in "ABCDEFabcdef" or self._ch.isdigit()):
            s += self._ch
            self._next()
        return s


# ── Singleton parser (stateful, but reset per call) ──────────────────────────

_parser = _LuaParser()


# ── Public API ───────────────────────────────────────────────────────────────


def decode_file(path: str | Path) -> dict | None:
    """Parse a KOReader ``.lua`` metadata file and return a Python dict.

    Returns ``None`` if the file cannot be decoded.
    The original header line is preserved under the ``"original_header"`` key
    so the file can be round-tripped with :func:`encode_file`.
    """
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    lines = text.split("\n", 1)
    if len(lines) < 2:
        return None
    header, body = lines

    # The body starts with "return " — strip it
    body = body[7:] if body.startswith("return ") else body
    # KOReader uses "--" as a comment marker inside strings in some versions
    body = body.replace("--", "\u2014")  # replace with em-dash temporarily

    result = _parser.decode(body)
    if not isinstance(result, dict):
        return None

    result["original_header"] = header
    return result


def encode_file(path: str | Path, data: dict) -> None:
    """Serialise *data* back to a KOReader-compatible ``.lua`` file.

    The ``"original_header"`` key is removed before encoding and written
    as the first line, preserving the file's original first line.
    """
    data = dict(data)  # shallow copy — don't mutate caller's dict
    header = data.pop("original_header", "-- KOReader metadata")
    lua_body = _parser.encode(data)
    Path(path).write_text(
        f"{header}\nreturn {lua_body}",
        encoding="utf-8",
        newline="",
    )
