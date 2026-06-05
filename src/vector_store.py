import json
from pathlib import Path
from typing import List, Dict, Optional

import faiss
import numpy as np

from src.config import FAISS_INDEX_PATH, METADATA_PATH, VECTORSTORE_DIR, EMBEDDING_DIMENSION
from src.utils import ensure_dir


def build_faiss_index(embeddings: np.ndarray, chunks: List[Dict]) -> faiss.Index:
    """
    Build a FAISS IndexFlatIP (inner product = cosine similarity on normalized vectors)
    from the given embeddings and save it along with chunk metadata.

    Args:
        embeddings: numpy array of shape (n_chunks, embedding_dim), L2-normalized
        chunks: list of chunk dicts with metadata

    Returns:
        The built FAISS index.
    """
    ensure_dir(VECTORSTORE_DIR)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    # Save FAISS index to disk
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    print(f"FAISS index saved to: {FAISS_INDEX_PATH}")
    print(f"Index contains {index.ntotal} vectors with dimension {dim}")

    # Save chunk metadata as JSON
    metadata = []
    for chunk in chunks:
        metadata.append({
            "chunk_id": chunk["chunk_id"],
            "source_file": chunk["source_file"],
            "doc_title": chunk["doc_title"],
            "section_heading": chunk["section_heading"],
            "text": chunk["text"],
            "token_count": chunk["token_count"],
        })

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"Chunk metadata saved to: {METADATA_PATH} ({len(metadata)} chunks)")

    return index


def load_faiss_index() -> Optional[faiss.Index]:
    """
    Load the FAISS index from disk if it exists.

    Returns:
        FAISS index if found, None otherwise.
    """
    if not FAISS_INDEX_PATH.exists():
        print(f"FAISS index not found at: {FAISS_INDEX_PATH}")
        print("Run 'python scripts/build_index.py' first to create the index.")
        return None

    index = faiss.read_index(str(FAISS_INDEX_PATH))
    print(f"FAISS index loaded from: {FAISS_INDEX_PATH}")
    print(f"Index contains {index.ntotal} vectors, dimension {index.d}")
    return index


def load_metadata() -> Optional[List[Dict]]:
    """
    Load chunk metadata from JSON file.

    Returns:
        List of chunk metadata dicts if found, None otherwise.
    """
    if not METADATA_PATH.exists():
        print(f"Chunk metadata not found at: {METADATA_PATH}")
        return None

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print(f"Loaded metadata for {len(metadata)} chunks")
    return metadata


def index_exists() -> bool:
    """Check whether a saved FAISS index and metadata file exist."""
    return FAISS_INDEX_PATH.exists() and METADATA_PATH.exists()
