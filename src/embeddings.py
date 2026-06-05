from typing import List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL_NAME, EMBEDDING_DIMENSION


_model: Optional[SentenceTransformer] = None


def load_embedding_model() -> SentenceTransformer:
    """
    Load the BGE embedding model (cached after first load).

    Returns a sentence-transformers model instance.
    The model is cached globally so it's only loaded once.
    """
    global _model
    if _model is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL_NAME} ...")
        try:
            _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
            print(f"Model loaded. Output dimension: {_model.get_embedding_dimension()}")
        except Exception as e:
            print(f"Error loading embedding model '{EMBEDDING_MODEL_NAME}': {e}")
            print("Check your internet connection — the model downloads on first use.")
            raise
    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    """
    Embed a list of texts using the BGE model.

    BGE models benefit from adding the 'Represent this sentence for searching: '
    prefix for retrieval tasks (per BAAI's official usage instructions).
    For indexing we do NOT add the prefix; for queries we DO (handled in retriever).

    Returns a numpy array of shape (len(texts), embedding_dim) with L2-normalized vectors.
    """
    model = load_embedding_model()
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,  # L2-normalize for cosine similarity via inner product
    )
    return np.array(embeddings, dtype=np.float32)


def embed_query(text: str) -> np.ndarray:
    """
    Embed a single query string with the retrieval prefix for BGE models.

    BGE models perform best when queries are prefixed with:
      "Represent this sentence for searching: "
    """
    model = load_embedding_model()
    # BGE official instruction prefix for retrieval
    prefixed = f"Represent this sentence for searching: {text}"
    embedding = model.encode(
        prefixed,
        normalize_embeddings=True,
    )
    return np.array([embedding], dtype=np.float32)
