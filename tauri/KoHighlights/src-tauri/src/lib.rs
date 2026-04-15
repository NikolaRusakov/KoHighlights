mod commands;
mod error;
mod exporter;
mod lua;
mod merger;
mod models;
mod platform;
mod scanner;
mod store;

pub use error::{AppError, Result};
pub use models::*;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            // scan
            commands::scan::scan_directory,
            commands::scan::load_from_archive,
            commands::scan::get_app_data_dir,
            // books
            commands::books::archive_books,
            commands::books::delete_books_info,
            commands::books::delete_books_and_files,
            commands::books::get_missing_books,
            commands::books::save_book,
            commands::books::delete_from_archive,
            // highlights
            commands::highlights::delete_highlight,
            commands::highlights::update_highlight_comment,
            commands::highlights::get_highlights_for_book,
            commands::highlights::copy_to_clipboard,
            // filter
            commands::filter::filter_books,
            commands::filter::filter_highlights,
            // export
            commands::export::export_books,
            // merge
            commands::merge::can_merge,
            commands::merge::merge_two_books,
            // notes
            commands::notes::create_note,
            commands::notes::get_note,
            commands::notes::list_notes,
            commands::notes::update_note,
            commands::notes::delete_note,
            commands::notes::list_notes_for_highlight,
            // settings
            commands::settings::load_settings,
            commands::settings::save_settings,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
