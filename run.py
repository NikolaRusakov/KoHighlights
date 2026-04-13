"""Development runner — add all src/ paths to sys.path and launch the app.

Usage:
    python run.py

This avoids needing ``pip install`` during development.  All polylith
component sources are added to sys.path so ``import kohighlights.*`` works.
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).parent

_SRC_PATHS = [
    "components/models/src",
    "components/lua_codec/src",
    "components/book_store/src",
    "components/file_scanner/src",
    "components/highlight_exporter/src",
    "components/highlight_merger/src",
    "components/use_cases/src",
    "components/ui/src",
    "bases/app/src",
]

for rel in _SRC_PATHS:
    p = str(_ROOT / rel)
    if p not in sys.path:
        sys.path.insert(0, p)

from kohighlights.app.main import run  # noqa: E402

if __name__ == "__main__":
    run()
