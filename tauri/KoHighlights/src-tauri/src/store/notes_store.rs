use duckdb::Connection;
use std::path::Path;

use crate::error::{AppError, Result};
use crate::models::Note;

pub struct NotesStore {
    conn: Connection,
}

impl NotesStore {
    pub fn new(path: &Path) -> Result<Self> {
        let conn = Connection::open(path.to_string_lossy().to_string()).map_err(|e| AppError::DuckDB(e.to_string()))?;

        // Create notes table
        conn.execute_batch(
            "CREATE SEQUENCE IF NOT EXISTS notes_id_seq START 1;
             CREATE TABLE IF NOT EXISTS notes (
                id         BIGINT    PRIMARY KEY DEFAULT nextval('notes_id_seq'),
                title      VARCHAR   NOT NULL DEFAULT '',
                content    TEXT      NOT NULL DEFAULT '',
                book_md5   VARCHAR,
                page_id    VARCHAR,
                created_at TIMESTAMP NOT NULL DEFAULT now(),
                updated_at TIMESTAMP NOT NULL DEFAULT now()
             );
             CREATE INDEX IF NOT EXISTS idx_notes_book ON notes(book_md5);
             CREATE INDEX IF NOT EXISTS idx_notes_highlight ON notes(book_md5, page_id)
                 WHERE book_md5 IS NOT NULL AND page_id IS NOT NULL;",
        ).map_err(|e| AppError::DuckDB(e.to_string()))?;

        Ok(NotesStore { conn })
    }

    pub fn create_note(&self, title: &str, content: &str, book_md5: Option<&str>, page_id: Option<&str>) -> Result<Note> {
        let mut stmt = self
            .conn
            .prepare("INSERT INTO notes (title, content, book_md5, page_id) VALUES (?, ?, ?, ?) RETURNING *")
            .map_err(|e| AppError::DuckDB(e.to_string()))?;

        let note = stmt
            .query_row(duckdb::params![title, content, book_md5, page_id], |row| {
                Ok(Note {
                    id: row.get(0)?,
                    title: row.get(1)?,
                    content: row.get(2)?,
                    book_md5: row.get(3)?,
                    page_id: row.get(4)?,
                    created_at: row.get(5)?,
                    updated_at: row.get(6)?,
                })
            })
            .map_err(|e| AppError::DuckDB(e.to_string()))?;

        Ok(note)
    }

    pub fn get_note(&self, id: i64) -> Result<Option<Note>> {
        let mut stmt = self
            .conn
            .prepare("SELECT * FROM notes WHERE id = ?")
            .map_err(|e| AppError::DuckDB(e.to_string()))?;

        let result = stmt
            .query_row(duckdb::params![id], |row| {
                Ok(Note {
                    id: row.get(0)?,
                    title: row.get(1)?,
                    content: row.get(2)?,
                    book_md5: row.get(3)?,
                    page_id: row.get(4)?,
                    created_at: row.get(5)?,
                    updated_at: row.get(6)?,
                })
            });

        result.map(Some).map_err(|e| AppError::DuckDB(e.to_string()))
    }

    pub fn list_notes(&self, book_md5: Option<&str>) -> Result<Vec<Note>> {
        let query = if let Some(md5) = book_md5 {
            format!("SELECT * FROM notes WHERE book_md5 = '{}' ORDER BY updated_at DESC", md5)
        } else {
            "SELECT * FROM notes ORDER BY updated_at DESC".to_string()
        };

        let mut stmt = self.conn.prepare(&query).map_err(|e| AppError::DuckDB(e.to_string()))?;
        let notes = stmt
            .query_map([], |row| {
                Ok(Note {
                    id: row.get(0)?,
                    title: row.get(1)?,
                    content: row.get(2)?,
                    book_md5: row.get(3)?,
                    page_id: row.get(4)?,
                    created_at: row.get(5)?,
                    updated_at: row.get(6)?,
                })
            })
            .map_err(|e| AppError::DuckDB(e.to_string()))?;

        let mut result = Vec::new();
        for note in notes {
            result.push(note.map_err(|e| AppError::DuckDB(e.to_string()))?);
        }
        Ok(result)
    }

    pub fn update_note(&self, id: i64, title: &str, content: &str) -> Result<Note> {
        let mut stmt = self
            .conn
            .prepare("UPDATE notes SET title = ?, content = ?, updated_at = now() WHERE id = ? RETURNING *")
            .map_err(|e| AppError::DuckDB(e.to_string()))?;

        let note = stmt
            .query_row(duckdb::params![title, content, id], |row| {
                Ok(Note {
                    id: row.get(0)?,
                    title: row.get(1)?,
                    content: row.get(2)?,
                    book_md5: row.get(3)?,
                    page_id: row.get(4)?,
                    created_at: row.get(5)?,
                    updated_at: row.get(6)?,
                })
            })
            .map_err(|e| AppError::DuckDB(e.to_string()))?;

        Ok(note)
    }

    pub fn delete_note(&self, id: i64) -> Result<()> {
        self.conn
            .execute("DELETE FROM notes WHERE id = ?", duckdb::params![id])
            .map_err(|e| AppError::DuckDB(e.to_string()))?;
        Ok(())
    }

    pub fn list_notes_for_highlight(&self, book_md5: &str, page_id: &str) -> Result<Vec<Note>> {
        let query = format!(
            "SELECT * FROM notes WHERE book_md5 = '{}' AND page_id = '{}' ORDER BY created_at DESC",
            book_md5, page_id
        );
        let mut stmt = self.conn.prepare(&query).map_err(|e| AppError::DuckDB(e.to_string()))?;
        let notes = stmt
            .query_map([], |row| {
                Ok(Note {
                    id: row.get(0)?,
                    title: row.get(1)?,
                    content: row.get(2)?,
                    book_md5: row.get(3)?,
                    page_id: row.get(4)?,
                    created_at: row.get(5)?,
                    updated_at: row.get(6)?,
                })
            })
            .map_err(|e| AppError::DuckDB(e.to_string()))?;

        let mut result = Vec::new();
        for note in notes {
            result.push(note.map_err(|e| AppError::DuckDB(e.to_string()))?);
        }
        Ok(result)
    }
}
