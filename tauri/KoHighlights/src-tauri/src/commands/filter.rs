use crate::error::Result;
use crate::models::{Book, Highlight};

#[tauri::command]
pub fn filter_books(books: Vec<Book>, filter_text: String, filter_type: String) -> Result<Vec<Book>> {
    // TODO: implement
    Ok(books)
}

#[tauri::command]
pub fn filter_highlights(highlights: Vec<Highlight>, filter_text: String, filter_type: String) -> Result<Vec<Highlight>> {
    // TODO: implement
    Ok(highlights)
}
