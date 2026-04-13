#!/usr/bin/env bash
# Install all components in editable mode for local development.
# Run from the repo root: bash dev_install.sh
set -e

echo "Installing KoHighlights (Flet rewrite) in development mode..."

pip install flet requests beautifulsoup4

# Install each component as a namespace package (editable)
for src_dir in \
  components/models/src \
  components/lua_codec/src \
  components/book_store/src \
  components/file_scanner/src \
  components/highlight_exporter/src \
  components/highlight_merger/src \
  components/use_cases/src \
  components/ui/src \
  bases/app/src
do
  echo "  → $src_dir"
  pip install --no-build-isolation -e "$src_dir" 2>/dev/null || true
done

echo ""
echo "Done. Run the app with:"
echo "  python -m kohighlights.app.main"
echo "  or: python run.py"
