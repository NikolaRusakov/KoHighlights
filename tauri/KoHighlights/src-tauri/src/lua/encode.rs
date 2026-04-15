use serde_json::Value as JsonValue;
use std::path::Path;

use crate::error::Result;

pub fn encode_value(val: &JsonValue, depth: usize) -> String {
    let tab = "    ".repeat(depth);
    let tab_outer = if depth > 0 { "    ".repeat(depth - 1) } else { String::new() };

    match val {
        JsonValue::Null => "nil".to_string(),
        JsonValue::Bool(b) => if *b { "true" } else { "false" }.to_string(),
        JsonValue::Number(n) => n.to_string(),
        JsonValue::String(s) => {
            // Escape quotes and backslashes
            let escaped = s.replace('\\', "\\\\").replace('"', "\\\"");
            format!("\"{}\"", escaped)
        }
        JsonValue::Array(arr) => {
            if arr.is_empty() {
                "{}".to_string()
            } else {
                let items: Vec<String> = arr
                    .iter()
                    .map(|v| format!("{}{}", tab, encode_value(v, depth + 1)))
                    .collect();
                format!("{{\n{}\n{}}}", items.join(",\n"), tab_outer)
            }
        }
        JsonValue::Object(map) => {
            if map.is_empty() {
                "{}".to_string()
            } else {
                let items: Vec<String> = map
                    .iter()
                    .map(|(k, v)| {
                        let key = if k.parse::<i64>().is_ok() {
                            format!("[{}]", k)
                        } else {
                            format!("[\"{}\"]", k.replace('"', "\\\""))
                        };
                        format!("{}{} = {}", tab, key, encode_value(v, depth + 1))
                    })
                    .collect();
                format!("{{\n{}\n{}}}", items.join(",\n"), tab_outer)
            }
        }
    }
}

pub fn encode_file(path: &Path, header: &str, data: &JsonValue) -> Result<()> {
    let body = encode_value(data, 0);
    let content = format!("{}\nreturn {}\n", header, body);
    std::fs::write(path, content)?;
    Ok(())
}
