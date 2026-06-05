import re
from typing import List, Dict

import tiktoken

from src.config import CHUNK_MAX_TOKENS, CHUNK_OVERLAP_TOKENS

# Tokenizer for counting tokens (cl100k_base is the encoding used by GPT-4 / text-embedding-3)
# It works well as a general-purpose tokenizer for English text chunking.
ENCODING = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """Return the number of tokens in a text string."""
    return len(ENCODING.encode(text))


def split_into_sections(text: str) -> List[Dict]:
    """
    Split document text into sections based on '## ' headings.

    Returns a list of dicts:
      {
        "heading": "Section Title" or "",
        "content": "section body text"
      }
    """
    sections = []
    # Pattern matches lines starting with '## ' (level-2 headings)
    pattern = r"^(##\s+.+)$"
    lines = text.splitlines()
    current_heading = ""
    current_content = []

    for line in lines:
        if re.match(pattern, line.strip()):
            if current_content or current_heading:
                sections.append({
                    "heading": current_heading,
                    "content": "\n".join(current_content).strip(),
                })
            current_heading = line.strip().lstrip("# ").strip()
            current_content = []
        else:
            current_content.append(line)

    # Don't forget the last section
    if current_content or current_heading:
        sections.append({
            "heading": current_heading,
            "content": "\n".join(current_content).strip(),
        })

    return sections


def recursive_chunk_text(text: str, max_tokens: int = CHUNK_MAX_TOKENS) -> List[str]:
    """
    Recursively split text into chunks that fit within max_tokens.

    Strategy:
      1. If text fits within max_tokens, return it as a single chunk.
      2. Otherwise, try to split on double newlines (paragraphs).
      3. If that's not enough, split on single newlines.
      4. As a last resort, split on sentences.
      5. As a final fallback, split on spaces.
    """
    if count_tokens(text) <= max_tokens:
        return [text]

    # Try splitting on double newlines (paragraph breaks)
    paragraphs = re.split(r"\n\s*\n", text)
    if len(paragraphs) > 1:
        return _merge_chunks(paragraphs, max_tokens)

    # Try splitting on single newlines
    lines = text.splitlines()
    if len(lines) > 1:
        return _merge_chunks(lines, max_tokens)

    # Try splitting on sentence boundaries
    sentences = re.split(r"(?<=[.!?])\s+", text)
    if len(sentences) > 1:
        return _merge_chunks(sentences, max_tokens)

    # Last resort: split on spaces
    words = text.split()
    return _merge_chunks(words, max_tokens)


def _merge_chunks(segments: List[str], max_tokens: int) -> List[str]:
    """
    Merge a list of text segments into chunks that each fit within max_tokens.
    Segments are greedily combined until the token limit is reached.
    """
    chunks = []
    current_chunk = []

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        # Check how many tokens we'd have if we added this segment
        test_text = " ".join(current_chunk + [segment])
        if current_chunk and count_tokens(test_text) > max_tokens:
            # Save current chunk and start a new one
            chunks.append(" ".join(current_chunk))
            current_chunk = [segment]
        else:
            current_chunk.append(segment)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks if chunks else [""]


def add_overlap(chunks: List[str], overlap_tokens: int = CHUNK_OVERLAP_TOKENS) -> List[str]:
    """
    Add overlap between consecutive chunks by prepending the tail of the
    previous chunk to the start of the current chunk.
    """
    if len(chunks) <= 1 or overlap_tokens <= 0:
        return chunks

    overlapped = []
    for i in range(len(chunks)):
        if i == 0:
            overlapped.append(chunks[i])
        else:
            # Take the last `overlap_tokens` tokens from the previous chunk
            prev_tokens = ENCODING.encode(chunks[i - 1])
            overlap_text = ENCODING.decode(prev_tokens[-overlap_tokens:]) if len(prev_tokens) > overlap_tokens else chunks[i - 1]
            # Prepend overlap text to current chunk (if it doesn't already start with it)
            if not chunks[i].startswith(overlap_text[-50:]):
                overlapped.append(overlap_text + " " + chunks[i])
            else:
                overlapped.append(chunks[i])

    return overlapped


def chunk_documents(documents: List[Dict]) -> List[Dict]:
    """
    Take a list of documents (from load_markdown_documents) and return
    a list of chunk dicts with full metadata.

    Each chunk dict has:
      - chunk_id: unique identifier
      - source_file: source filename
      - doc_title: document title
      - section_heading: section heading (may be empty)
      - text: the chunk text
      - token_count: number of tokens
    """
    all_chunks = []

    for doc in documents:
        sections = split_into_sections(doc["text"])

        for section in sections:
            section_text = section["content"]
            if not section_text:
                continue

            # Recursively chunk the section content
            raw_chunks = recursive_chunk_text(section_text, CHUNK_MAX_TOKENS)

            # Add overlap between chunks within the same section
            raw_chunks = add_overlap(raw_chunks, CHUNK_OVERLAP_TOKENS)

            for chunk_text in raw_chunks:
                if not chunk_text.strip():
                    continue

                chunk_id = f"{doc['source_file']}_{len(all_chunks):04d}"

                all_chunks.append({
                    "chunk_id": chunk_id,
                    "source_file": doc["source_file"],
                    "doc_title": doc["title"],
                    "section_heading": section["heading"],
                    "text": chunk_text.strip(),
                    "token_count": count_tokens(chunk_text),
                })

    print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
    return all_chunks
