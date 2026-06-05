from typing import List, Dict, Optional

import numpy as np

from src.config import RETRIEVAL_TOP_K
from src.embeddings import embed_query
from src.vector_store import load_faiss_index, load_metadata


def retrieve(query: str, top_k: int = RETRIEVAL_TOP_K) -> List[Dict]:
    """
    Retrieve the top-k most relevant chunks for a given query.

    Args:
        query: the user's question or search query
        top_k: number of chunks to return (default: 5)

    Returns:
        List of dicts, each containing:
          - chunk_id
          - text
          - source_file
          - doc_title
          - section_heading
          - similarity_score

    Raises:
        RuntimeError: if the FAISS index or metadata cannot be loaded.
    """
    index = load_faiss_index()
    metadata = load_metadata()

    if index is None:
        raise RuntimeError(
            "FAISS index not found. Run 'python scripts/build_index.py' first."
        )
    if metadata is None:
        raise RuntimeError(
            "Chunk metadata not found. Run 'python scripts/build_index.py' first."
        )

    # Embed the query (with BGE retrieval prefix)
    query_vec = embed_query(query)  # shape: (1, dim)

    # Search the FAISS index
    scores, indices = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue  # FAISS returns -1 when there are fewer results than top_k
        chunk_meta = metadata[idx]
        results.append({
            "chunk_id": chunk_meta["chunk_id"],
            "text": chunk_meta["text"],
            "source_file": chunk_meta["source_file"],
            "doc_title": chunk_meta["doc_title"],
            "section_heading": chunk_meta["section_heading"],
            "similarity_score": round(float(score), 4),
        })

    return results
