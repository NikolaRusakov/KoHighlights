use crate::error::Result;
use crate::models::{Book, MergeResult};

#[tauri::command]
pub fn can_merge(book_a: Book, book_b: Book) -> Result<bool> {
    Ok(crate::merger::can_merge(&book_a, &book_b))
}

#[tauri::command]
pub fn merge_two_books(
    mut book_a: Book,
    mut book_b: Book,
    do_merge: bool,
    do_sync_position: bool,
) -> Result<MergeResult> {
    crate::merger::merge_two_books(&mut book_a, &mut book_b, do_merge, do_sync_position)
}
