export interface Highlight {
  text: string;
  page: number;
  date: string;
  chapter: string;
  comment: string;
  page_id: string;
}

export interface Book {
  path: string;
  title: string;
  authors: string;
  series: string;
  language: string;
  pages: number;
  keywords: string;
  highlights: Highlight[];
  rating: string;
  status: string;
  percent_finished: number;
  modified_date: string;
  cre_dom_version: string;
  md5: string;
  book_path: string;
  raw_data: unknown;
  original_header: string;
}

export interface Note {
  id: number;
  title: string;
  content: string;
  book_md5: string | null;
  page_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface AppSettings {
  last_dir: string;
  db_path: string;
  view_mode: 'books' | 'highlights';
  sort_col: string;
  sort_asc: boolean;
  window_width: number;
  window_height: number;
  db_mode: boolean;
  show_exit_confirm: boolean;
  highlight_by_page: boolean;
  skip_version: string;
  opened_times: number;
  toolbar_size: number;
}

export interface MergeResult {
  added: number;
  duplicates: number;
  book_a: Book;
  book_b: Book;
}

export interface ArchiveResult {
  added: number;
  skipped_no_highlights: number;
  skipped_old_format: number;
}

export interface ExportResult {
  saved: number;
  skipped: number;
  output_paths: string[];
}
