use crate::error::Result;
use crate::models::{Book, ExportResult, Highlight};
use std::fs;
use std::path::{Path, PathBuf};

/// Export books to various formats (TXT/HTML/CSV/MD/JSON)
pub fn export_books(
    books: &[Book],
    format: &str,
    mode: &str,
    output_dir: &str,
    show_page: bool,
    show_date: bool,
    show_chapter: bool,
    show_comment: bool,
    sort_by_page: bool,
) -> Result<ExportResult> {
    fs::create_dir_all(output_dir)?;

    let mut saved = 0;
    let mut skipped = 0;
    let mut output_paths = Vec::new();

    if mode == "one" {
        // All books in one file
        let path = export_books_merged(
            books,
            format,
            output_dir,
            show_page,
            show_date,
            show_chapter,
            show_comment,
            sort_by_page,
        )?;
        output_paths.push(path.to_string_lossy().to_string());
        saved = books.len() as usize;
    } else {
        // One file per book
        for book in books {
            if book.highlights.is_empty() {
                skipped += 1;
                continue;
            }
            let path = export_book(
                book,
                format,
                output_dir,
                show_page,
                show_date,
                show_chapter,
                show_comment,
                sort_by_page,
            )?;
            output_paths.push(path.to_string_lossy().to_string());
            saved += 1;
        }
    }

    Ok(ExportResult {
        saved,
        skipped,
        output_paths,
    })
}

fn export_book(
    book: &Book,
    format: &str,
    output_dir: &str,
    show_page: bool,
    show_date: bool,
    show_chapter: bool,
    show_comment: bool,
    sort_by_page: bool,
) -> Result<PathBuf> {
    let mut sorted_highs = book.highlights.clone();
    sorted_highs.sort_by(|a, b| {
        if sort_by_page {
            (a.page, &a.date).cmp(&(b.page, &b.date))
        } else {
            (&a.date, a.page).cmp(&(&b.date, b.page))
        }
    });

    let title = if book.authors.is_empty() {
        book.title.clone()
    } else {
        format!("{} - {}", book.authors, book.title)
    };

    let stem = sanitize(&title);
    let out_dir = Path::new(output_dir);
    let (ext, content) = match format {
        "txt" => ("txt", export_txt(&title, &sorted_highs, show_page, show_date, show_chapter, show_comment)),
        "html" => ("html", export_html(&book.title, &book.authors, &sorted_highs, show_page, show_date, show_chapter, show_comment)),
        "csv" => ("csv", export_csv(&book.title, &book.authors, &sorted_highs)),
        "md" => ("md", export_md(&book.title, &book.authors, &sorted_highs, show_page, show_date, show_chapter, show_comment)),
        "json" => ("json", export_json(&book.title, &book.authors, &sorted_highs)),
        _ => return Err(crate::error::AppError::Logic(format!("Unknown format: {}", format))),
    };

    let mut out_path = out_dir.join(format!("{}.{}", stem, ext));

    // Avoid clobbering NO TITLE files
    if title.contains("NO TITLE") {
        let mut idx = 1;
        while out_path.exists() {
            out_path = out_dir.join(format!("{}[{:02}].{}", stem, idx, ext));
            idx += 1;
        }
    }

    fs::write(&out_path, content)?;
    Ok(out_path)
}

fn export_books_merged(
    books: &[Book],
    format: &str,
    output_dir: &str,
    show_page: bool,
    show_date: bool,
    show_chapter: bool,
    show_comment: bool,
    sort_by_page: bool,
) -> Result<PathBuf> {
    let out_dir = Path::new(output_dir);
    let (ext, content) = match format {
        "txt" => {
            let mut all_highs = Vec::new();
            for book in books {
                let mut highs = book.highlights.clone();
                highs.sort_by(|a, b| {
                    if sort_by_page {
                        (a.page, &a.date).cmp(&(b.page, &b.date))
                    } else {
                        (&a.date, a.page).cmp(&(&b.date, b.page))
                    }
                });
                all_highs.extend(highs);
            }
            let mut content = String::from("KoHighlights Export\n");
            content.push_str(&"=".repeat(80));
            content.push('\n');
            for book in books {
                content.push_str(&format!("\n\n{} - {}\n", book.authors, book.title));
                content.push_str(&"-".repeat(80));
                content.push('\n');
            }
            ("txt", content)
        }
        "json" => {
            let mut records = Vec::new();
            for book in books {
                for h in &book.highlights {
                    records.push(serde_json::json!({
                        "title": book.title,
                        "authors": book.authors,
                        "page": h.page,
                        "date": h.date,
                        "chapter": h.chapter,
                        "text": h.text,
                        "comment": h.comment,
                    }));
                }
            }
            ("json", serde_json::to_string_pretty(&records).unwrap_or_default())
        }
        _ => {
            let mut content = String::new();
            for book in books {
                content.push_str(&format!("\n\n{} - {}\n", book.authors, book.title));
            }
            (ext, content)
        }
    };

    let out_path = out_dir.join(format!("KoHighlights_export.{}", ext));
    fs::write(&out_path, content)?;
    Ok(out_path)
}

fn export_txt(title: &str, highs: &[Highlight], show_page: bool, show_date: bool, show_chapter: bool, show_comment: bool) -> String {
    let mut content = format!("{}\n{}\n{}\n\n", "-".repeat(80), title, "-".repeat(80));
    for h in highs {
        if show_page || show_date {
            let page = if show_page && h.page > 0 { format!("p.{}", h.page) } else { String::new() };
            if !page.is_empty() || show_date {
                content.push_str(&format!("{}  {}\n", page, if show_date { &h.date } else { "" }));
            }
        }
        if show_chapter && !h.chapter.is_empty() {
            content.push_str(&format!("[{}]\n", h.chapter));
        }
        content.push_str(&format!("{}\n", h.text));
        if show_comment && !h.comment.is_empty() {
            content.push_str(&format!("{}\n", h.comment));
        }
        content.push('\n');
    }
    content
}

fn export_html(title: &str, authors: &str, highs: &[Highlight], show_page: bool, show_date: bool, show_chapter: bool, show_comment: bool) -> String {
    let mut content = String::from("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n<style>\nbody { font-family: Georgia, serif; max-width: 860px; margin: 0 auto; }\n</style>\n</head>\n<body>\n");
    content.push_str(&format!("<h2>{}</h2>\n<h3>{}</h3>\n", title, authors));
    for h in highs {
        content.push_str("<div class=\"high-block\">\n");
        if show_page || show_date {
            let page = if show_page && h.page > 0 { format!("p.{}", h.page) } else { String::new() };
            content.push_str(&format!("<p><small>{} {}</small></p>\n", page, if show_date { &h.date } else { "" }));
        }
        if show_chapter && !h.chapter.is_empty() {
            content.push_str(&format!("<h4>{}</h4>\n", h.chapter));
        }
        content.push_str(&format!("<p>{}</p>\n", h.text.replace('\n', "<br/>")));
        if show_comment && !h.comment.is_empty() {
            content.push_str(&format!("<p><em>{}</em></p>\n", h.comment));
        }
        content.push_str("</div>\n");
    }
    content.push_str("</body>\n</html>");
    content
}

fn export_csv(title: &str, authors: &str, highs: &[Highlight]) -> String {
    let mut content = String::from("Title\tAuthors\tPage\tDate\tChapter\tHighlight\tComment\n");
    for h in highs {
        let cols = vec![
            title.to_string(),
            authors.to_string(),
            h.page.to_string(),
            h.date.clone(),
            h.chapter.clone(),
            h.text.clone(),
            h.comment.clone(),
        ];
        content.push_str(&cols.join("\t"));
        content.push('\n');
    }
    content
}

fn export_md(title: &str, authors: &str, highs: &[Highlight], show_page: bool, show_date: bool, show_chapter: bool, show_comment: bool) -> String {
    let mut content = format!("## {}\n##### {}\n---\n", title, authors);
    for h in highs {
        if show_page || show_date {
            let page = if show_page && h.page > 0 { format!("p.{}", h.page) } else { String::new() };
            if !page.is_empty() || show_date {
                content.push_str(&format!("*{} {}*  \n", page, if show_date { &h.date } else { "" }));
            }
        }
        if show_chapter && !h.chapter.is_empty() {
            content.push_str(&format!("***{}***  \n", h.chapter));
        }
        content.push_str(&format!("{}  \n", h.text.replace('\n', "  \n")));
        if show_comment && !h.comment.is_empty() {
            content.push_str(&format!("{}  \n", h.comment.replace('\n', "  \n")));
        }
        content.push_str("\n");
    }
    content
}

fn export_json(title: &str, authors: &str, highs: &[Highlight]) -> String {
    let records: Vec<_> = highs.iter().map(|h| {
        serde_json::json!({
            "title": title,
            "authors": authors,
            "page": h.page,
            "date": h.date,
            "chapter": h.chapter,
            "text": h.text,
            "comment": h.comment,
        })
    }).collect();
    serde_json::to_string_pretty(&records).unwrap_or_default()
}

fn sanitize(name: &str) -> String {
    name.chars()
        .map(|c| match c {
            '/' | ':' | '*' | '?' | '"' | '<' | '>' | '|' | '\\' => '_',
            _ => c,
        })
        .collect()
}
