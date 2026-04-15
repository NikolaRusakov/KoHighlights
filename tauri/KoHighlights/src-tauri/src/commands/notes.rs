use crate::error::Result;
use crate::models::Note;

#[tauri::command]
pub fn create_note(title: String, content: String, book_md5: Option<String>, page_id: Option<String>) -> Result<Note> {
    // TODO: implement
    Ok(Note {
        id: 0,
        title,
        content,
        book_md5,
        page_id,
        created_at: String::new(),
        updated_at: String::new(),
    })
}

#[tauri::command]
pub fn get_note(id: i64) -> Result<Option<Note>> {
    // TODO: implement
    Ok(None)
}

#[tauri::command]
pub fn list_notes(book_md5: Option<String>) -> Result<Vec<Note>> {
    // TODO: implement
    Ok(vec![])
}

#[tauri::command]
pub fn update_note(id: i64, title: String, content: String) -> Result<Note> {
    // TODO: implement
    Ok(Note {
        id,
        title,
        content,
        book_md5: None,
        page_id: None,
        created_at: String::new(),
        updated_at: String::new(),
    })
}

#[tauri::command]
pub fn delete_note(id: i64) -> Result<()> {
    // TODO: implement
    Ok(())
}

#[tauri::command]
pub fn list_notes_for_highlight(book_md5: String, page_id: String) -> Result<Vec<Note>> {
    // TODO: implement
    Ok(vec![])
}
