use tauri::AppHandle;
use crate::error::Result;
use crate::models::AppSettings;
use crate::store::SettingsStore;
use crate::platform;

#[tauri::command]
pub fn load_settings(app: AppHandle) -> Result<AppSettings> {
    let settings_path = platform::get_settings_path(&app)?;
    let store = SettingsStore::new(&settings_path)?;
    store.load()
}

#[tauri::command]
pub fn save_settings(settings: AppSettings, app: AppHandle) -> Result<()> {
    let settings_path = platform::get_settings_path(&app)?;
    let store = SettingsStore::new(&settings_path)?;
    store.save(&settings)
}
