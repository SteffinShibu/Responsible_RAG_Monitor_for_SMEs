from typing import List, Dict

from src.retriever import retrieve
from src.generator import generate_answer


def answer_query(query: str, top_k: int = 5) -> Dict:
    """
    Run the full RAG pipeline: retrieve relevant chunks, generate an answer.

    Args:
        query: the user's question.
        top_k: number of chunks to retrieve (default: 5).

    Returns:
        A dict with:
          - query: the original question
          - answer: the generated answer text
          - sources: list of retrieved chunk dicts (with metadata and scores)

    Raises:
        RuntimeError: if the FAISS index is missing.
        ValueError: if the query is empty, the API key is missing, or the query
                    references a file the model cannot process.
        Exception: if the Groq API call fails.
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    # Step 1: Retrieve relevant chunks
    chunks = retrieve(query, top_k=top_k)

    if not chunks:
        return {
            "query": query,
            "answer": (
                "I could not find any relevant policy documents for your question. "
                "Please try rephrasing or ask a different question."
            ),
            "sources": [],
        }

    # Step 2: Generate an answer using Groq
    answer = generate_answer(query, chunks)

    return {
        "query": query,
        "answer": answer,
        "sources": chunks,
    }
