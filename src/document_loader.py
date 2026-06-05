from pathlib import Path
from typing import List, Dict

from src.config import RAW_DOCUMENTS_DIR


def extract_title(text: str) -> str:
    """Extract the document title from the first '# ' heading in the text.

    Skips headings that look like filenames (end with .md).
    Also checks inside ```code blocks``` for a real title.
    """
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            title = stripped.lstrip("# ").strip().strip("`")
            if title and not title.lower().endswith(".md"):
                return title
    # Fallback: look inside code blocks
    inside_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            inside_code = not inside_code
            continue
        if inside_code and stripped.startswith("# ") and not stripped.startswith("## "):
            title = stripped.lstrip("# ").strip()
            if title:
                return title
    return "Untitled Document"


def load_markdown_documents() -> List[Dict]:
    """
    Read all .md files from the raw_documents directory.

    Returns a list of dicts:
      {
        "source_file": "filename.md",
        "title": "Document Title",
        "text": "full raw markdown text"
      }
    """
    if not RAW_DOCUMENTS_DIR.exists():
        print(f"Error: raw_documents directory not found at: {RAW_DOCUMENTS_DIR}")
        print("Please ensure data/raw_documents/ exists with .md files inside.")
        return []

    md_files = sorted(RAW_DOCUMENTS_DIR.glob("*.md"))

    if not md_files:
        print(f"Warning: No .md files found in {RAW_DOCUMENTS_DIR}")
        return []

    documents = []
    for md_path in md_files:
        text = md_path.read_text(encoding="utf-8").strip()
        if not text:
            print(f"Warning: {md_path.name} is empty — skipping.")
            continue

        title = extract_title(text)

        documents.append({
            "source_file": md_path.name,
            "title": title,
            "text": text,
            "file_path": str(md_path),
        })

    print(f"Loaded {len(documents)} documents from {RAW_DOCUMENTS_DIR}")
    return documents
