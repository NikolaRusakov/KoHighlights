use std::path::PathBuf;
use tauri::{AppHandle, Manager};

use crate::error::Result;

pub fn get_app_data_dir(app: &AppHandle) -> Result<PathBuf> {
    app.path()
        .app_data_dir()
        .map_err(|e| crate::error::AppError::Path(e.to_string()))
}

pub fn get_db_path(app: &AppHandle) -> Result<PathBuf> {
    Ok(get_app_data_dir(app)?.join("data.db"))
}

pub fn get_notes_db_path(app: &AppHandle) -> Result<PathBuf> {
    Ok(get_app_data_dir(app)?.join("notes.duckdb"))
}

pub fn get_settings_path(app: &AppHandle) -> Result<PathBuf> {
    Ok(get_app_data_dir(app)?.join("settings.json"))
}
