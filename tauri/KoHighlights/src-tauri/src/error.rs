use serde::Serialize;

#[derive(Debug, thiserror::Error, Serialize)]
pub enum AppError {
    #[error("Lua error: {0}")]
    Lua(String),

    #[error("SQLite error: {0}")]
    Sqlite(#[from] rusqlite::Error),

    #[error("DuckDB error: {0}")]
    DuckDB(String),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),

    #[error("{0}")]
    Logic(String),

    #[error("Path error: {0}")]
    Path(String),
}

impl From<mlua::Error> for AppError {
    fn from(err: mlua::Error) -> Self {
        AppError::Lua(err.to_string())
    }
}

impl From<duckdb::Error> for AppError {
    fn from(err: duckdb::Error) -> Self {
        AppError::DuckDB(err.to_string())
    }
}

pub type Result<T> = std::result::Result<T, AppError>;
