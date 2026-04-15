use mlua::{Lua, Value as LuaValue};
use serde_json::{json, Map, Value as JsonValue};
use std::path::Path;

use crate::error::{AppError, Result};

/// Decode KOReader .lua file to serde_json::Value + original_header
pub fn decode_file(path: &Path) -> Result<(JsonValue, String)> {
    let text = std::fs::read_to_string(path)?;

    // Extract first line as original_header (KOReader metadata comment)
    let mut lines = text.splitn(2, '\n');
    let original_header = lines.next().unwrap_or("").to_string();
    let body = lines.next().unwrap_or(&text);

    // mlua: evaluate the Lua code directly
    let lua = Lua::new();
    let value: LuaValue = lua.load(body).eval().map_err(|e| AppError::Lua(e.to_string()))?;

    let json = lua_value_to_json(&lua, value)?;
    Ok((json, original_header))
}

fn lua_value_to_json(lua: &Lua, val: LuaValue) -> Result<JsonValue> {
    match val {
        LuaValue::Nil => Ok(JsonValue::Null),
        LuaValue::Boolean(b) => Ok(JsonValue::Bool(b)),
        LuaValue::Integer(i) => Ok(json!(i)),
        LuaValue::Number(f) => {
            if f.fract() == 0.0 && f.is_finite() {
                Ok(json!(f as i64))
            } else {
                Ok(json!(f))
            }
        }
        LuaValue::String(s) => {
            let s_str = s.to_str().map_err(|e| AppError::Lua(format!("String conversion error: {}", e)))?;
            Ok(JsonValue::String(s_str.to_string()))
        }
        LuaValue::Table(t) => {
            // Check if table is array-like (sequential integer keys) or object-like
            let mut map = Map::new();
            let mut int_entries = Vec::new();
            let mut has_non_int_keys = false;
            let mut max_int_key: i64 = 0;

            for pair in t.clone().pairs::<LuaValue, LuaValue>() {
                let (k, v) = pair.map_err(|e| AppError::Lua(e.to_string()))?;
                let json_val = lua_value_to_json(lua, v)?;

                match k {
                    LuaValue::Integer(i) => {
                        int_entries.push((i, json_val));
                        max_int_key = max_int_key.max(i);
                    }
                    LuaValue::String(ks) => {
                        let key = ks.to_str().map_err(|e| AppError::Lua(e.to_string()))?;
                        map.insert(key.to_string(), json_val);
                        has_non_int_keys = true;
                    }
                    _ => {
                        has_non_int_keys = true;
                    }
                }
            }

            // If all keys are sequential integers starting from 1, return array
            if !has_non_int_keys && !int_entries.is_empty() {
                int_entries.sort_by_key(|(i, _)| *i);
                let is_sequential = int_entries.iter().enumerate().all(|(idx, (i, _))| *i == (idx + 1) as i64);

                if is_sequential {
                    let arr: Vec<JsonValue> = int_entries.into_iter().map(|(_, v)| v).collect();
                    return Ok(JsonValue::Array(arr));
                }
            }

            // Otherwise, return object with string keys
            for (i, v) in int_entries {
                map.insert(i.to_string(), v);
            }
            Ok(JsonValue::Object(map))
        }
        _ => Ok(JsonValue::Null),
    }
}
