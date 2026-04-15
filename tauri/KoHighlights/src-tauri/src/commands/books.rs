use crate::error::Result;
use crate::models::{Book, ArchiveResult};

#[tauri::command]
pub fn archive_books(books: Vec<Book>) -> Result<ArchiveResult> {
    // TODO: implement
    Ok(ArchiveResult {
        added: 0,
        skipped_no_highlights: 0,
        skipped_old_format: 0,
    })
}

#[tauri::command]
pub fn delete_books_info(books: Vec<Book>) -> Result<()> {
    // TODO: implement
    Ok(())
}

#[tauri::command]
pub fn delete_books_and_files(books: Vec<Book>) -> Result<()> {
    // TODO: implement
    Ok(())
}

#[tauri::command]
pub fn get_missing_books(books: Vec<Book>) -> Result<Vec<Book>> {
    // TODO: implement
    Ok(vec![])
}

#[tauri::command]
pub fn save_book(book: Book) -> Result<()> {
    // TODO: implement
    Ok(())
}

#[tauri::command]
pub fn delete_from_archive(md5: String) -> Result<()> {
    // TODO: implement
    Ok(())
}
