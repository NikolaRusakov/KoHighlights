use std::collections::{HashMap, HashSet};
use serde_json::{json, Value as JsonValue};

use crate::error::Result;
use crate::lua::encode_file;
use crate::models::{Book, Highlight, MergeResult};

pub fn can_merge(book_a: &Book, book_b: &Book) -> bool {
    !book_a.title.is_empty()
        && !book_b.title.is_empty()
        && book_a.title.to_lowercase().trim() == book_b.title.to_lowercase().trim()
        && book_a.cre_dom_version == book_b.cre_dom_version
}

pub fn merge_two_books(
    book_a: &mut Book,
    book_b: &mut Book,
    do_merge: bool,
    do_sync_position: bool,
) -> Result<MergeResult> {
    if !can_merge(book_a, book_b) {
        return Err(crate::error::AppError::Logic(format!(
            "Cannot merge books: '{}' vs '{}'",
            book_a.title, book_b.title
        )));
    }

    let mut result = MergeResult {
        added: 0,
        duplicates: 0,
        book_a: book_a.clone(),
        book_b: book_b.clone(),
    };

    if do_merge {
        let keys_a: HashSet<String> = book_a.highlights.iter().map(highlight_key).collect();
        let keys_b: HashSet<String> = book_b.highlights.iter().map(highlight_key).collect();

        let new_in_a: Vec<_> = book_b
            .highlights
            .iter()
            .filter(|h| !keys_a.contains(&highlight_key(h)))
            .cloned()
            .collect();

        let new_in_b: Vec<_> = book_a
            .highlights
            .iter()
            .filter(|h| !keys_b.contains(&highlight_key(h)))
            .cloned()
            .collect();

        let duplicates = book_a.highlights.len() + book_b.highlights.len() - new_in_a.len() - new_in_b.len();

        // Update in-memory models
        book_a.highlights.extend(new_in_a);
        book_a.highlights = dedup(&book_a.highlights);

        book_b.highlights.extend(new_in_b);
        book_b.highlights = dedup(&book_b.highlights);

        result.book_a = book_a.clone();
        result.book_b = book_b.clone();
        result.added = new_in_a.len() + new_in_b.len();
        result.duplicates = duplicates;

        // Write back to disk
        write_book_back(book_a)?;
        write_book_back(book_b)?;
    }

    if do_sync_position {
        if book_a.percent_finished >= book_b.percent_finished {
            sync_position(book_b, book_a)?;
        } else {
            sync_position(book_a, book_b)?;
        }
        result.book_a = book_a.clone();
        result.book_b = book_b.clone();
    }

    Ok(result)
}

fn highlight_key(h: &Highlight) -> String {
    if !h.page_id.is_empty() {
        h.page_id.clone()
    } else {
        let text_part = if h.text.len() > 60 {
            &h.text[..60]
        } else {
            &h.text
        };
        format!("{}|{}", h.page, text_part)
    }
}

fn dedup(highlights: &[Highlight]) -> Vec<Highlight> {
    let mut seen = HashSet::new();
    let mut result = Vec::new();
    for h in highlights {
        let key = highlight_key(h);
        if !seen.contains(&key) {
            seen.insert(key);
            result.push(h.clone());
        }
    }
    result
}

fn sync_position(follower: &mut Book, leader: &Book) -> Result<()> {
    follower.percent_finished = leader.percent_finished;

    if let Some(obj) = follower.raw_data.as_object_mut() {
        obj.insert("percent_finished".to_string(), json!(leader.percent_finished));

        // Sync position keys if present in leader
        for key in &["last_page", "last_xpointer", "last_position"] {
            if let Some(val) = leader.raw_data.get(*key) {
                obj.insert(key.to_string(), val.clone());
            }
        }
    }

    write_book_back(follower)?;
    Ok(())
}

fn write_book_back(book: &Book) -> Result<()> {
    let mut raw = book.raw_data.clone();
    let obj = raw
        .as_object_mut()
        .ok_or_else(|| crate::error::AppError::Logic("raw_data must be object".to_string()))?;

    // Rebuild highlight structure from highlights list
    let mut highs: HashMap<String, JsonValue> = HashMap::new();
    for h in &book.highlights {
        let page_key = h.page.to_string();
        let page_obj = highs
            .entry(page_key)
            .or_insert_with(|| json!({}));

        if let Some(page_map) = page_obj.as_object_mut() {
            let idx = page_map.len();
            page_map.insert(
                idx.to_string(),
                json!({
                    "text": h.text,
                    "datetime": h.date,
                    "chapter": h.chapter,
                    "note": h.comment,
                    "pageno": h.page_id,
                }),
            );
        }
    }

    // Convert HashMap to JsonValue for assignment
    let highs_json = serde_json::to_value(&highs)?;
    obj.insert("highlight".to_string(), highs_json);

    encode_file(
        std::path::Path::new(&book.path),
        &book.original_header,
        &raw,
    )?;

    Ok(())
}
