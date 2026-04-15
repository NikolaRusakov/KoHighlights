use rusqlite::{Connection, params};
use std::path::Path;

use crate::error::Result;
use crate::models::Book;

pub struct BookStore {
    conn: Connection,
}

impl BookStore {
    pub fn new(path: &Path) -> Result<Self> {
        let conn = Connection::open(path)?;
        conn.execute_batch(
            "CREATE TABLE IF NOT EXISTS books (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                md5   TEXT UNIQUE NOT NULL,
                date  TEXT,
                path  TEXT,
                data  TEXT
            )",
        )?;
        Ok(BookStore { conn })
    }

    pub fn upsert(&self, md5: &str, path: &str, date: &str, data: &serde_json::Value) -> Result<()> {
        let data_str = serde_json::to_string(data)?;
        self.conn.execute(
            "INSERT OR REPLACE INTO books (md5, date, path, data) VALUES (?1, ?2, ?3, ?4)",
            params![md5, date, path, data_str],
        )?;
        Ok(())
    }

    pub fn delete(&self, md5: &str) -> Result<()> {
        self.conn.execute("DELETE FROM books WHERE md5 = ?1", params![md5])?;
        Ok(())
    }

    pub fn all_records(&self) -> Result<Vec<(String, String, String, serde_json::Value)>> {
        let mut stmt = self.conn.prepare("SELECT md5, path, date, data FROM books")?;
        let records = stmt.query_map([], |row| {
            let md5: String = row.get(0)?;
            let path: String = row.get(1)?;
            let date: String = row.get(2)?;
            let data_str: String = row.get(3)?;
            let data = serde_json::from_str(&data_str).unwrap_or(serde_json::json!({}));
            Ok((md5, path, date, data))
        })?;

        let mut result = Vec::new();
        for record in records {
            result.push(record?);
        }
        Ok(result)
    }

    pub fn get_by_md5(&self, md5: &str) -> Result<Option<serde_json::Value>> {
        let mut stmt = self.conn.prepare("SELECT data FROM books WHERE md5 = ?1")?;
        let result = stmt.query_row(params![md5], |row| {
            let data_str: String = row.get(0)?;
            Ok(serde_json::from_str(&data_str).unwrap_or(serde_json::json!({})))
        });

        match result {
            Ok(data) => Ok(Some(data)),
            Err(rusqlite::Error::QueryReturnedNoRows) => Ok(None),
            Err(e) => Err(crate::error::AppError::from(e)),
        }
    }

    pub fn count(&self) -> Result<u32> {
        let count: u32 = self.conn.query_row("SELECT COUNT(*) FROM books", [], |row| row.get(0))?;
        Ok(count)
    }

    pub fn vacuum(&self) -> Result<()> {
        self.conn.execute("VACUUM", [])?;
        Ok(())
    }
}
