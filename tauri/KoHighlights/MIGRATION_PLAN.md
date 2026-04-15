# KoHighlights: Flet/Python → Tauri v2 + React 19 Migration

## Context
KoHighlights is a KOReader highlight manager. Current implementation: Flet (Python) app with modular Polylith architecture in `bases/app/` + `components/`. Migrating to Tauri v2 + React 19 + TypeScript with iOS/Android support via Tauri Mobile. Existing Tauri scaffold at `tauri/KoHighlights/` — Tauri v2, React 19, bare greet demo only.

DuckDB replaces SQLite for a new **notes** feature (standalone notes + per-highlight notes). Book archive stays SQLite for backward compatibility.

---

## Critical Architectural Decisions

### Lua codec: use `mlua` (Option B)
- `mlua` crate with `features = ["lua54", "vendored"]` embeds Lua 5.4 statically
- Evaluate `.lua` file via `Lua::new().load(body).eval()` → Lua table → `serde_json::Value`
- Eliminates need to port the 285-line recursive-descent parser
- Works on all platforms including Android/iOS
- Encode-back: custom Rust formatter (simpler than parsing)

### raw_data round-trip
`Book.raw_data: serde_json::Value` is the opaque Lua dict that flows frontend → command → encode_file. Commands `delete_highlight`, `update_highlight_comment` mutate it in Rust and return updated Book. Frontend replaces its Zustand copy. `save_book` writes to disk.

### DuckDB mobile caveat
If DuckDB `bundled` feature fails to cross-compile for Android NDK or iOS clang, fall back to second `rusqlite` DB (`notes.db`). Schema is identical with `INTEGER PRIMARY KEY AUTOINCREMENT` instead of sequences. **Test this in Phase 1 before committing.**

---

## Rust Backend Structure

```
src-tauri/src/
├── lib.rs                    # Builder, plugins, invoke_handler wiring
├── main.rs                   # unchanged
├── error.rs                  # AppError: Lua/Sqlite/DuckDB/Io/Json/Logic variants + Serialize
├── models/mod.rs             # Book, Highlight, Note, AppSettings, MergeResult, ArchiveResult, ExportResult
├── lua/
│   ├── decode.rs             # mlua: .lua file → serde_json::Value + original_header
│   └── encode.rs             # serde_json::Value → Lua table string
├── scanner/mod.rs            # walkdir: *.sdr/metadata.*.lua → Vec<Book>
├── store/
│   ├── book_store.rs         # rusqlite: books(id, md5, date, path, data TEXT)
│   ├── notes_store.rs        # duckdb: notes table
│   └── settings_store.rs     # read/write settings.json (plain JSON)
├── exporter/mod.rs           # TXT/HTML/CSV/MD/JSON formatters
├── merger/mod.rs             # bidirectional merge, dedup by page_id
├── platform/mod.rs           # get_app_data_dir/db_path/notes_db_path/settings_path
└── commands/
    ├── scan_commands.rs
    ├── book_commands.rs
    ├── highlight_commands.rs
    ├── filter_commands.rs
    ├── export_commands.rs
    ├── merge_commands.rs
    ├── settings_commands.rs
    └── notes_commands.rs
```

---

## Cargo.toml Dependencies

```toml
tauri = { version = "2", features = ["devtools"] }
tauri-plugin-opener = "2"
tauri-plugin-fs = "2"
tauri-plugin-dialog = "2"
tauri-plugin-permissions = "2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
mlua = { version = "0.10", features = ["lua54", "vendored"] }
rusqlite = { version = "0.31", features = ["bundled"] }
duckdb = { version = "1.1", features = ["bundled"] }
walkdir = "2"
chrono = { version = "0.4", features = ["serde"] }
thiserror = "1"
```

---

## All Tauri Commands

### Scan
```rust
scan_directory(path: String, app: AppHandle) -> Result<Vec<Book>, String>
// emits "scan-progress" events: { path: String, count: usize }
load_from_archive(state: State<AppStateHandle>) -> Result<Vec<Book>, String>
get_app_data_dir(app: AppHandle) -> Result<String, String>
```

### Books
```rust
archive_books(books: Vec<Book>, state: State) -> Result<ArchiveResult, String>
delete_books_info(books: Vec<Book>) -> Result<(), String>       // remove .sdr dirs
delete_books_and_files(books: Vec<Book>) -> Result<(), String>  // .sdr + ebook file
get_missing_books(books: Vec<Book>) -> Result<Vec<Book>, String>
save_book(book: Book) -> Result<(), String>                     // encode_file → disk
get_book_from_archive(md5: String, state: State) -> Result<Option<Book>, String>
delete_from_archive(md5: String, state: State) -> Result<(), String>
```

### Highlights
```rust
delete_highlight(book: Book, highlight: Highlight) -> Result<Book, String>
update_highlight_comment(book: Book, highlight: Highlight, new_comment: String) -> Result<Book, String>
get_highlights_for_book(book: Book) -> Result<Vec<Highlight>, String>
copy_to_clipboard(text: String, app: AppHandle) -> Result<(), String>
```

### Filter (synchronous — no async needed)
```rust
filter_books(books: Vec<Book>, filter_text: String, filter_type: String) -> Result<Vec<Book>, String>
filter_highlights(highlights: Vec<Highlight>, filter_text: String, filter_type: String) -> Result<Vec<Highlight>, String>
```

### Export
```rust
export_books(books: Vec<Book>, format: String, mode: String, output_dir: String,
             show_page: bool, show_date: bool, show_chapter: bool, show_comment: bool,
             sort_by_page: bool) -> Result<ExportResult, String>
```

### Merge
```rust
can_merge(book_a: Book, book_b: Book) -> Result<bool, String>
merge_two_books(book_a: Book, book_b: Book, do_merge: bool, do_sync_position: bool) -> Result<MergeResult, String>
// MergeResult includes updated book_a and book_b so React can replace in state
```

### Settings
```rust
load_settings(app: AppHandle) -> Result<AppSettings, String>
save_settings(settings: AppSettings, app: AppHandle) -> Result<(), String>
```

### Notes (DuckDB)
```rust
create_note(title: String, content: String, book_md5: Option<String>, page_id: Option<String>, state: State) -> Result<Note, String>
get_note(id: i64, state: State) -> Result<Option<Note>, String>
list_notes(book_md5: Option<String>, state: State) -> Result<Vec<Note>, String>
update_note(id: i64, title: String, content: String, state: State) -> Result<Note, String>
delete_note(id: i64, state: State) -> Result<(), String>
list_notes_for_highlight(book_md5: String, page_id: String, state: State) -> Result<Vec<Note>, String>
```

---

## DuckDB Notes Schema

```sql
CREATE SEQUENCE IF NOT EXISTS notes_id_seq START 1;
CREATE TABLE IF NOT EXISTS notes (
    id         BIGINT    PRIMARY KEY DEFAULT nextval('notes_id_seq'),
    title      VARCHAR   NOT NULL DEFAULT '',
    content    TEXT      NOT NULL DEFAULT '',
    book_md5   VARCHAR,  -- NULL for standalone notes
    page_id    VARCHAR,  -- NULL for book-level (not highlight-specific)
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_notes_book ON notes(book_md5);
CREATE INDEX IF NOT EXISTS idx_notes_highlight ON notes(book_md5, page_id)
    WHERE book_md5 IS NOT NULL AND page_id IS NOT NULL;
```

---

## React Frontend Structure

### npm packages to add
```bash
bun add react-router-dom@6 zustand@5 @tanstack/react-query@5 \
    @tanstack/react-table@8 @tanstack/react-virtual@3 \
    tailwindcss@3 autoprefixer postcss \
    @tauri-apps/plugin-fs@2 @tauri-apps/plugin-dialog@2 @tauri-apps/plugin-permissions@2
# Then: bunx shadcn-ui@latest init
# Then add: table button dialog input select dropdown-menu badge
```

### Directory structure
```
src/
├── types/index.ts            # TypeScript mirrors of Rust structs
├── api/                      # thin invoke() wrappers per domain
│   ├── scan.ts, books.ts, highlights.ts, filter.ts
│   ├── export.ts, merge.ts, settings.ts, notes.ts
├── store/app-store.ts        # Zustand: books, selectedBooks, displayedBooks,
│                             # highlights, viewMode, dbMode, filter, isScanning, settings
├── hooks/                    # TanStack Query per domain
│   ├── useScan.ts, useBooks.ts, useNotes.ts
│   ├── useExport.ts, useMerge.ts, useSettings.ts
├── pages/
│   ├── BooksPage.tsx         # "/"
│   ├── HighlightsPage.tsx    # "/highlights"
│   └── NotesPage.tsx         # "/notes"
└── components/
    ├── layout/AppToolbar.tsx, FilterBar.tsx
    ├── books/BooksTable.tsx, BookInfoPanel.tsx, HighlightsPanel.tsx
    ├── highlights/HighlightsTable.tsx
    ├── notes/NotesList.tsx, NoteEditor.tsx
    └── dialogs/ExportDialog.tsx, CommentDialog.tsx, MergeDialog.tsx,
               DeleteConfirmDialog.tsx, AboutDialog.tsx
```

### State strategy
- **Zustand**: UI state (selections, view mode, filter, scanning flag, books list)
- **TanStack Query**: async mutations (scan, export, merge, notes CRUD)
- **`listen('scan-progress')`**: incremental book additions during scan

---

## Mobile Configuration

### Capabilities
**`capabilities/default.json`** (desktop): `core:default, opener:default, fs:allow-read-file, fs:allow-write-file, fs:allow-read-dir, fs:allow-create-dir, fs:allow-remove-file, fs:allow-remove-dir, dialog:allow-open, dialog:allow-save, dialog:allow-message`

**`capabilities/mobile.json`**: `platforms: ["android", "ios"]` + same fs/dialog + `permissions:allow-request, permissions:allow-check`

### AndroidManifest.xml (after `tauri android init`)
```xml
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32"/>
<uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="28"/>
```
Before scan: call `request_scan_permission` command → `tauri-plugin-permissions` requests `MANAGE_EXTERNAL_STORAGE`.

### Info.plist (after `tauri ios init`)
```xml
<key>UIFileSharingEnabled</key><true/>
<key>LSSupportsOpeningDocumentsInPlace</key><true/>
<key>NSDocumentsFolderUsageDescription</key>
<string>KoHighlights needs access to find KOReader highlight files.</string>
```
iOS scan: use `dialog` plugin's `open()` → `UIDocumentPickerViewController` → security-scoped URL → `scan_directory`.

---

## Platform Storage Paths (`platform/mod.rs`)

```rust
// tauri::path::app_data_dir() resolves to:
// Android:  /data/user/0/solutions.doto.kohighlights-rs/files/
// iOS:      <sandbox>/Library/Application Support/
// macOS:    ~/Library/Application Support/solutions.doto.kohighlights-rs/
// Linux:    ~/.local/share/solutions.doto.kohighlights-rs/
// Windows:  %APPDATA%\solutions.doto.kohighlights-rs\
pub fn get_db_path(app: &AppHandle) -> PathBuf      // → data dir / data.db
pub fn get_notes_db_path(app: &AppHandle) -> PathBuf // → data dir / notes.duckdb
pub fn get_settings_path(app: &AppHandle) -> PathBuf // → data dir / settings.json
```

---

## Implementation Phases (ordered)

### Phase 1: Rust Core (no Tauri, unit-testable)
1. Add Cargo.toml deps, `cargo check` — confirm `mlua` vendored + `duckdb` bundled compile
2. `error.rs` — AppError enum
3. `models/mod.rs` — all structs with serde
4. `lua/decode.rs` — mlua decode. **Test against real `.lua` fixture files**
5. `lua/encode.rs` — round-trip: `decode → encode → decode` must be identical
6. `scanner/mod.rs` — walkdir + Book construction
7. `store/book_store.rs` — rusqlite with Python-compatible schema
8. `store/settings_store.rs` — plain JSON read/write
9. `store/notes_store.rs` — DuckDB init + CRUD
10. `exporter/mod.rs` — all 5 formats. Test output vs Python on same fixture
11. `merger/mod.rs` — dedup by page_id, bidirectional, write-back
12. `platform/mod.rs` — path helpers

### Phase 2: Tauri Commands
13. Implement all command modules (8 files in `commands/`)
14. Wire `lib.rs`: plugins + managed state + invoke_handler
15. Add capabilities files
16. `cargo build` desktop target, fix errors
17. Test with stub React via `invoke()` in browser devtools

### Phase 3: React Foundation
18. Install npm packages + shadcn/ui
19. Configure Tailwind + tsconfig path alias `@/` → `src/`
20. `types/index.ts`, `api/` layer, `store/app-store.ts`, `hooks/`

### Phase 4: BooksPage UI
21. `AppToolbar.tsx` — scan, export menu, merge menu, delete menu, archive, clear, filter, view toggle, db toggle, about
22. `FilterBar.tsx` — text + type dropdown
23. `BooksTable.tsx` — TanStack Table + useVirtualizer, 8 cols, checkbox, sort, dbl-click opens
24. `BookInfoPanel.tsx` — collapsible
25. `HighlightsPanel.tsx` — card list + hover actions
26. `BooksPage.tsx` — 3:2 panel layout
27. All dialogs: Comment, Delete, Export, About

### Phase 5: HighlightsPage + NotesPage
28. `HighlightsTable.tsx` — 7 cols, virtual scroll
29. `HighlightsPage.tsx`
30. `NotesList.tsx` + `NoteEditor.tsx`
31. `NotesPage.tsx`

### Phase 6: Mobile
32. `bunx tauri android init` → edit AndroidManifest.xml
33. `bunx tauri ios init` → edit Info.plist
34. Add `capabilities/mobile.json`
35. `bunx tauri android dev` — test on emulator/device
36. `bunx tauri ios dev` (macOS only) — test on simulator
37. Fix mobile path resolution, permission flows, SAF edge cases

### Phase 7: Polish
38. Scan progress streaming via `app.emit` + React `listen()`
39. Window size persistence on close event
40. `MergeDialog.tsx` with merge/sync options
41. tauri.conf.json: proper title, min-size (800×500)
42. App icons

---

## Key Files to Modify/Create

**Rust (create):**
- `tauri/KoHighlights/src-tauri/Cargo.toml` — add all deps
- `tauri/KoHighlights/src-tauri/src/lib.rs` — replace greet with full wiring
- `tauri/KoHighlights/src-tauri/src/` — all new modules

**Rust (reference for ports):**
- `components/lua_codec/src/kohighlights/lua_codec/core.py` — decode/encode logic
- `components/highlight_merger/src/kohighlights/highlight_merger/merger.py` — merge/dedup
- `components/file_scanner/src/kohighlights/file_scanner/scanner.py` — walk logic + field mapping
- `components/book_store/src/kohighlights/book_store/sqlite_store.py` — schema

**Capabilities (modify):**
- `tauri/KoHighlights/src-tauri/capabilities/default.json`
- `tauri/KoHighlights/src-tauri/capabilities/mobile.json` (create)

**React (create):**
- Everything under `tauri/KoHighlights/src/`

**Mobile (create after init):**
- `src-tauri/gen/android/app/src/main/AndroidManifest.xml`
- `src-tauri/gen/apple/KoHighlights/Info.plist`

---

## Verification

1. **Desktop**: `bunx tauri dev` → scan a real KOReader `.sdr` folder, verify books appear, edit a comment, delete a highlight, re-scan to confirm change persisted on disk
2. **Archive**: archive books → toggle to archived mode → verify books load from SQLite
3. **Export**: export to each of 5 formats → verify file contents match Python output format
4. **Merge**: select 2 copies of same book → merge → verify highlight union in both .lua files
5. **Notes**: create standalone note, create note attached to a highlight, verify DuckDB persistence
6. **Android**: `bunx tauri android dev` → request permission → scan SD card folder → verify works
7. **iOS**: `bunx tauri ios dev` → use file picker → scan → verify works in simulator
