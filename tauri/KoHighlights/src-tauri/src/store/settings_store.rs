use std::path::{Path, PathBuf};

use crate::error::Result;
use crate::models::AppSettings;

pub struct SettingsStore {
    settings_path: PathBuf,
}

impl SettingsStore {
    pub fn new(settings_path: &Path) -> Result<Self> {
        // Ensure parent directory exists
        if let Some(parent) = settings_path.parent() {
            std::fs::create_dir_all(parent)?;
        }
        Ok(SettingsStore {
            settings_path: settings_path.to_path_buf(),
        })
    }

    pub fn load(&self) -> Result<AppSettings> {
        if self.settings_path.exists() {
            let content = std::fs::read_to_string(&self.settings_path)?;
            let settings = serde_json::from_str(&content)?;
            Ok(settings)
        } else {
            Ok(AppSettings::default())
        }
    }

    pub fn save(&self, settings: &AppSettings) -> Result<()> {
        let content = serde_json::to_string_pretty(settings)?;
        std::fs::write(&self.settings_path, content)?;
        Ok(())
    }
}
