use crate::error::Result;
use crate::models::{Book, ExportResult};

#[tauri::command]
pub fn export_books(
    books: Vec<Book>,
    format: String,
    mode: String,
    output_dir: String,
    show_page: bool,
    show_date: bool,
    show_chapter: bool,
    show_comment: bool,
    sort_by_page: bool,
) -> Result<ExportResult> {
    crate::exporter::export_books(&books, &format, &mode, &output_dir, show_page, show_date, show_chapter, show_comment, sort_by_page)
}
