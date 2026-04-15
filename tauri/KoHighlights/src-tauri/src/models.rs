use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Highlight {
    pub text: String,
    pub page: i32,
    pub date: String,
    pub chapter: String,
    pub comment: String,
    pub page_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Book {
    pub path: String,
    pub title: String,
    pub authors: String,
    pub series: String,
    pub language: String,
    pub pages: i32,
    pub keywords: String,
    pub highlights: Vec<Highlight>,
    pub rating: String,
    pub status: String,
    pub percent_finished: f64,
    pub modified_date: String,
    pub cre_dom_version: String,
    pub md5: String,
    pub book_path: String,
    pub raw_data: serde_json::Value,
    pub original_header: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Note {
    pub id: i64,
    pub title: String,
    pub content: String,
    pub book_md5: Option<String>,
    pub page_id: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppSettings {
    pub last_dir: String,
    pub db_path: String,
    pub view_mode: String,
    pub sort_col: String,
    pub sort_asc: bool,
    pub window_width: u32,
    pub window_height: u32,
    pub db_mode: bool,
    pub show_exit_confirm: bool,
    pub highlight_by_page: bool,
    pub skip_version: String,
    pub opened_times: u32,
    pub toolbar_size: u32,
}

impl Default for AppSettings {
    fn default() -> Self {
        Self {
            last_dir: String::new(),
            db_path: String::new(),
            view_mode: "books".to_string(),
            sort_col: "modified".to_string(),
            sort_asc: false,
            window_width: 1200,
            window_height: 750,
            db_mode: false,
            show_exit_confirm: true,
            highlight_by_page: true,
            skip_version: "0.0.0.0".to_string(),
            opened_times: 0,
            toolbar_size: 48,
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MergeResult {
    pub added: usize,
    pub duplicates: usize,
    pub book_a: Book,
    pub book_b: Book,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ArchiveResult {
    pub added: usize,
    pub skipped_no_highlights: usize,
    pub skipped_old_format: usize,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ExportResult {
    pub saved: usize,
    pub skipped: usize,
    pub output_paths: Vec<String>,
}
