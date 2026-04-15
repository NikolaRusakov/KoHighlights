use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};
use walkdir::WalkDir;
use md5;

use crate::error::Result;
use crate::lua::decode_file;
use crate::models::{Book, Highlight};

/// Scan directory for KOReader .lua metadata files and yield Books
pub fn scan_for_books(root: &Path) -> Result<Vec<Book>> {
    let mut books = Vec::new();

    for entry in WalkDir::new(root)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| !e.path().components().any(|c| {
            if let std::path::Component::Normal(n) = c {
                n.to_string_lossy().starts_with('.')
            } else {
                false
            }
        }))
    {
        let path = entry.path();

        // Look for *.sdr/metadata.*.lua files
        if path.file_name()
            .and_then(|n| n.to_str())
            .map(|n| n.starts_with("metadata.") && n.ends_with(".lua"))
            .unwrap_or(false)
        {
            // Check parent is .sdr directory
            if let Some(parent) = path.parent() {
                if parent
                    .file_name()
                    .and_then(|n| n.to_str())
                    .map(|n| n.ends_with(".sdr"))
                    .unwrap_or(false)
                {
                    match decode_file(path) {
                        Ok((raw_data, original_header)) => {
                            if let Ok(book) = raw_to_book(path, raw_data, original_header) {
                                books.push(book);
                            }
                        }
                        Err(_) => continue,
                    }
                }
            }
        }
    }

    Ok(books)
}

/// Convert raw Lua dict to Book with highlights extracted
fn raw_to_book(path: &Path, raw_data: serde_json::Value, original_header: String) -> Result<Book> {
    let obj = raw_data.as_object().ok_or_else(|| {
        crate::error::AppError::Logic("raw_data must be object".to_string())
    })?;

    // Extract metadata fields from raw_data
    let title = obj
        .get("title")
        .or_else(|| obj.get("stats").and_then(|s| s.get("title")))
        .and_then(|v| v.as_str())
        .unwrap_or("NO TITLE FOUND")
        .to_string();

    let authors = obj
        .get("authors")
        .or_else(|| obj.get("stats").and_then(|s| s.get("authors")))
        .and_then(|v| v.as_str())
        .unwrap_or("NO AUTHOR FOUND")
        .to_string();

    let series = obj
        .get("series")
        .and_then(|v| v.as_str())
        .unwrap_or("")
        .to_string();

    let language = obj
        .get("language")
        .and_then(|v| v.as_str())
        .unwrap_or("")
        .to_string();

    let pages = obj
        .get("pages")
        .or_else(|| obj.get("stats").and_then(|s| s.get("pages")))
        .and_then(|v| v.as_i64())
        .unwrap_or(0) as i32;

    let keywords = obj
        .get("keywords")
        .and_then(|v| v.as_str())
        .unwrap_or("")
        .to_string();

    let rating = obj
        .get("summary")
        .and_then(|s| s.get("rating"))
        .and_then(|v| v.as_str())
        .map(|s| format!("{}★", s))
        .unwrap_or_default();

    let status = obj
        .get("summary")
        .and_then(|s| s.get("status"))
        .and_then(|v| v.as_str())
        .unwrap_or("")
        .to_string();

    let percent_finished = obj
        .get("percent_finished")
        .and_then(|v| v.as_f64())
        .unwrap_or(0.0);

    let cre_dom_version = obj
        .get("cre_dom_version")
        .and_then(|v| v.as_str())
        .unwrap_or("")
        .to_string();

    // Compute MD5 from path (fallback if partial_md5_checksum not in raw_data)
    let md5 = obj
        .get("partial_md5_checksum")
        .and_then(|v| v.as_str())
        .unwrap_or_else(|| {
            let digest = md5::compute(path.to_string_lossy().as_bytes());
            let hex = format!("{:x}", digest);
            &hex[..8.min(hex.len())]
        })
        .to_string();

    let modified_date = fs::metadata(path)
        .ok()
        .and_then(|m| m.modified().ok())
        .and_then(|t| {
            let duration = t
                .duration_since(std::time::UNIX_EPOCH)
                .ok()?;
            let secs = duration.as_secs() as i64;
            chrono::DateTime::<chrono::Utc>::from_timestamp(secs, 0).ok()
        })
        .map(|dt| dt.format("%Y-%m-%d %H:%M:%S").to_string())
        .unwrap_or_default();

    let book_path = path
        .parent()
        .and_then(|p| p.file_name())
        .and_then(|n| n.to_str())
        .map(|s| s.strip_suffix(".sdr").unwrap_or(s).to_string())
        .unwrap_or_default();

    // Extract highlights from raw_data
    let highlights = extract_highlights(obj);

    Ok(Book {
        path: path.to_string_lossy().to_string(),
        title,
        authors,
        series,
        language,
        pages,
        keywords,
        highlights,
        rating,
        status,
        percent_finished,
        modified_date,
        cre_dom_version,
        md5,
        book_path,
        raw_data,
        original_header,
    })
}

fn extract_highlights(obj: &serde_json::Map<String, serde_json::Value>) -> Vec<Highlight> {
    let mut highlights = Vec::new();

    if let Some(highlight_data) = obj.get("highlight") {
        // Dict format: {page: {idx: {text, datetime, chapter, note, pageno}}}
        if let Some(page_dict) = highlight_data.as_object() {
            for (page_key, page_val) in page_dict {
                let page = page_key.parse::<i32>().unwrap_or(0);

                if let Some(idx_dict) = page_val.as_object() {
                    for (_idx, h_val) in idx_dict {
                        if let Some(h_obj) = h_val.as_object() {
                            let text = h_obj
                                .get("text")
                                .and_then(|v| v.as_str())
                                .unwrap_or("")
                                .to_string();

                            let date = h_obj
                                .get("datetime")
                                .or_else(|| h_obj.get("date"))
                                .and_then(|v| v.as_str())
                                .unwrap_or("")
                                .to_string();

                            let chapter = h_obj
                                .get("chapter")
                                .and_then(|v| v.as_str())
                                .unwrap_or("")
                                .to_string();

                            let comment = h_obj
                                .get("note")
                                .or_else(|| h_obj.get("comment"))
                                .and_then(|v| v.as_str())
                                .unwrap_or("")
                                .to_string();

                            let page_id = h_obj
                                .get("pageno")
                                .or_else(|| h_obj.get("pos0"))
                                .and_then(|v| v.as_str())
                                .unwrap_or("")
                                .to_string();

                            highlights.push(Highlight {
                                text,
                                page,
                                date,
                                chapter,
                                comment,
                                page_id,
                            });
                        }
                    }
                }
            }
        }
    }

    // Also check for array format (newer KOReader)
    if let Some(highlight_array) = obj.get("highlights") {
        if let Some(arr) = highlight_array.as_array() {
            for h_val in arr {
                if let Some(h_obj) = h_val.as_object() {
                    let text = h_obj
                        .get("text")
                        .and_then(|v| v.as_str())
                        .unwrap_or("")
                        .to_string();

                    let page = h_obj.get("page").and_then(|v| v.as_i64()).unwrap_or(0) as i32;

                    let date = h_obj
                        .get("datetime")
                        .or_else(|| h_obj.get("date"))
                        .and_then(|v| v.as_str())
                        .unwrap_or("")
                        .to_string();

                    let chapter = h_obj
                        .get("chapter")
                        .and_then(|v| v.as_str())
                        .unwrap_or("")
                        .to_string();

                    let comment = h_obj
                        .get("note")
                        .or_else(|| h_obj.get("comment"))
                        .and_then(|v| v.as_str())
                        .unwrap_or("")
                        .to_string();

                    let page_id = h_obj
                        .get("pageno")
                        .or_else(|| h_obj.get("pos0"))
                        .and_then(|v| v.as_str())
                        .unwrap_or("")
                        .to_string();

                    highlights.push(Highlight {
                        text,
                        page,
                        date,
                        chapter,
                        comment,
                        page_id,
                    });
                }
            }
        }
    }

    highlights
}
