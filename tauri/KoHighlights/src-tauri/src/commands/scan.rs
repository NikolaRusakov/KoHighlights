use tauri::{AppHandle, State};
use std::path::Path;
use std::sync::Mutex;

use crate::error::Result;
use crate::models::{Book, AppSettings};
use crate::scanner;
use crate::store::{BookStore, SettingsStore};
use crate::platform;

#[tauri::command]
pub fn scan_directory(path: String) -> Result<Vec<Book>> {
    let root = Path::new(&path);
    scanner::scan_for_books(root)
}

#[tauri::command]
pub fn load_from_archive(app: AppHandle) -> Result<Vec<Book>> {
    let db_path = platform::get_db_path(&app)?;
    let store = BookStore::new(&db_path)?;
    let records = store.all_records()?;

    let mut books = Vec::new();
    for (md5, path, date, raw_data) in records {
        let book = Book {
            path,
            title: raw_data
                .get("title")
                .or_else(|| raw_data.get("stats").and_then(|s| s.get("title")))
                .and_then(|v| v.as_str())
                .unwrap_or("NO TITLE FOUND")
                .to_string(),
            authors: raw_data
                .get("authors")
                .or_else(|| raw_data.get("stats").and_then(|s| s.get("authors")))
                .and_then(|v| v.as_str())
                .unwrap_or("NO AUTHOR FOUND")
                .to_string(),
            series: raw_data
                .get("series")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            language: raw_data
                .get("language")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            pages: raw_data
                .get("pages")
                .or_else(|| raw_data.get("stats").and_then(|s| s.get("pages")))
                .and_then(|v| v.as_i64())
                .unwrap_or(0) as i32,
            keywords: raw_data
                .get("keywords")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            highlights: vec![],
            rating: raw_data
                .get("summary")
                .and_then(|s| s.get("rating"))
                .and_then(|v| v.as_str())
                .map(|s| format!("{}★", s))
                .unwrap_or_default(),
            status: raw_data
                .get("summary")
                .and_then(|s| s.get("status"))
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            percent_finished: raw_data
                .get("percent_finished")
                .and_then(|v| v.as_f64())
                .unwrap_or(0.0),
            modified_date: date,
            cre_dom_version: raw_data
                .get("cre_dom_version")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            md5,
            book_path: String::new(),
            raw_data,
            original_header: String::new(),
        };
        books.push(book);
    }

    Ok(books)
}

#[tauri::command]
pub fn get_app_data_dir(app: AppHandle) -> Result<String> {
    let path = platform::get_app_data_dir(&app)?;
    Ok(path.to_string_lossy().to_string())
}
