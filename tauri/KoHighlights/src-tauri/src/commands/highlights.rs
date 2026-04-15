use crate::error::Result;
use crate::models::{Book, Highlight};

#[tauri::command]
pub fn delete_highlight(book: Book, highlight: Highlight) -> Result<Book> {
    // TODO: implement
    Ok(book)
}

#[tauri::command]
pub fn update_highlight_comment(book: Book, highlight: Highlight, new_comment: String) -> Result<Book> {
    // TODO: implement
    Ok(book)
}

#[tauri::command]
pub fn get_highlights_for_book(book: Book) -> Result<Vec<Highlight>> {
    Ok(book.highlights)
}

#[tauri::command]
pub fn copy_to_clipboard(text: String) -> Result<()> {
    // TODO: implement
    Ok(())
}
