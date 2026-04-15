// API layer: thin wrappers around Tauri invoke() calls

import { invoke } from '@tauri-apps/api/core';
import {
  Book, Highlight, Note, AppSettings,
  MergeResult, ArchiveResult, ExportResult
} from '@/types';

// ── Scan commands ────────────────────────────────────────────────────
export const scanDirectory = (path: string): Promise<Book[]> =>
  invoke('scan_directory', { path });

export const loadFromArchive = (): Promise<Book[]> =>
  invoke('load_from_archive');

export const getAppDataDir = (): Promise<string> =>
  invoke('get_app_data_dir');

// ── Books commands ───────────────────────────────────────────────────
export const archiveBooks = (books: Book[]): Promise<ArchiveResult> =>
  invoke('archive_books', { books });

export const deleteBooksInfo = (books: Book[]): Promise<void> =>
  invoke('delete_books_info', { books });

export const deleteBooksAndFiles = (books: Book[]): Promise<void> =>
  invoke('delete_books_and_files', { books });

export const getMissingBooks = (books: Book[]): Promise<Book[]> =>
  invoke('get_missing_books', { books });

export const saveBook = (book: Book): Promise<void> =>
  invoke('save_book', { book });

export const deleteFromArchive = (md5: string): Promise<void> =>
  invoke('delete_from_archive', { md5 });

// ── Highlights commands ──────────────────────────────────────────────
export const deleteHighlight = (book: Book, highlight: Highlight): Promise<Book> =>
  invoke('delete_highlight', { book, highlight });

export const updateHighlightComment = (book: Book, highlight: Highlight, new_comment: string): Promise<Book> =>
  invoke('update_highlight_comment', { book, highlight, new_comment });

export const getHighlightsForBook = (book: Book): Promise<Highlight[]> =>
  invoke('get_highlights_for_book', { book });

export const copyToClipboard = (text: string): Promise<void> =>
  invoke('copy_to_clipboard', { text });

// ── Filter commands ──────────────────────────────────────────────────
export const filterBooks = (books: Book[], filter_text: string, filter_type: string): Promise<Book[]> =>
  invoke('filter_books', { books, filter_text, filter_type });

export const filterHighlights = (highlights: Highlight[], filter_text: string, filter_type: string): Promise<Highlight[]> =>
  invoke('filter_highlights', { highlights, filter_text, filter_type });

// ── Export commands ──────────────────────────────────────────────────
export const exportBooks = (
  books: Book[],
  format: string,
  mode: string,
  output_dir: string,
  show_page: boolean,
  show_date: boolean,
  show_chapter: boolean,
  show_comment: boolean,
  sort_by_page: boolean
): Promise<ExportResult> =>
  invoke('export_books', {
    books, format, mode, output_dir,
    show_page, show_date, show_chapter, show_comment, sort_by_page
  });

// ── Merge commands ───────────────────────────────────────────────────
export const canMerge = (book_a: Book, book_b: Book): Promise<boolean> =>
  invoke('can_merge', { book_a, book_b });

export const mergeTwoBooks = (
  book_a: Book,
  book_b: Book,
  do_merge: boolean,
  do_sync_position: boolean
): Promise<MergeResult> =>
  invoke('merge_two_books', { book_a, book_b, do_merge, do_sync_position });

// ── Notes commands ───────────────────────────────────────────────────
export const createNote = (
  title: string,
  content: string,
  book_md5?: string,
  page_id?: string
): Promise<Note> =>
  invoke('create_note', { title, content, book_md5, page_id });

export const getNote = (id: number): Promise<Note | null> =>
  invoke('get_note', { id });

export const listNotes = (book_md5?: string): Promise<Note[]> =>
  invoke('list_notes', { book_md5 });

export const updateNote = (id: number, title: string, content: string): Promise<Note> =>
  invoke('update_note', { id, title, content });

export const deleteNote = (id: number): Promise<void> =>
  invoke('delete_note', { id });

export const listNotesForHighlight = (book_md5: string, page_id: string): Promise<Note[]> =>
  invoke('list_notes_for_highlight', { book_md5, page_id });

// ── Settings commands ────────────────────────────────────────────────
export const loadSettings = (): Promise<AppSettings> =>
  invoke('load_settings');

export const saveSettings = (settings: AppSettings): Promise<void> =>
  invoke('save_settings', { settings });
