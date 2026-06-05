"""
Build the FAISS index from the raw Markdown documents.

Usage:
    python scripts/build_index.py

This script:
  1. Loads all .md files from data/raw_documents/
  2. Chunks them using token-based recursive chunking
  3. Embeds each chunk using the BGE embedding model
  4. Builds a FAISS index and saves it to vectorstore/faiss_index/
  5. Saves chunk metadata as JSON

If the index already exists, it will be rebuilt from scratch.
"""

import sys
from pathlib import Path

# Add project root to sys.path so we can import src modules
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.utils import check_dependencies, check_path_exists
from src.config import RAW_DOCUMENTS_DIR
from src.document_loader import load_markdown_documents
from src.chunker import chunk_documents
from src.embeddings import embed_texts
from src.vector_store import build_faiss_index


def main():
    print("=" * 60)
    print("Phase 1: Building FAISS Index from SME Policy Documents")
    print("=" * 60)

    # Check dependencies
    check_dependencies()

    # Step 1: Verify raw documents directory exists
    check_path_exists(RAW_DOCUMENTS_DIR, "Raw documents directory")

    # Step 2: Load documents
    print("\n[1/4] Loading documents...")
    documents = load_markdown_documents()
    if not documents:
        print("No documents found. Exiting.")
        sys.exit(1)

    # Step 3: Chunk documents
    print("\n[2/4] Chunking documents...")
    chunks = chunk_documents(documents)
    if not chunks:
        print("No chunks created. Check your document contents.")
        sys.exit(1)

    # Show a sample chunk
    print(f"\nSample chunk:")
    print(f"  chunk_id: {chunks[0]['chunk_id']}")
    print(f"  source_file: {chunks[0]['source_file']}")
    print(f"  doc_title: {chunks[0]['doc_title']}")
    print(f"  section_heading: {chunks[0]['section_heading']}")
    print(f"  token_count: {chunks[0]['token_count']}")
    print(f"  text preview: {chunks[0]['text'][:100]}...")

    # Step 4: Embed chunks
    print("\n[3/4] Embedding chunks with BGE model...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(texts)
    print(f"Generated {len(embeddings)} embeddings, each {embeddings.shape[1]}-dimensional")

    # Step 5: Build and save FAISS index
    print("\n[4/4] Building and saving FAISS index...")
    build_faiss_index(embeddings, chunks)

    print("\n" + "=" * 60)
    print("Done! FAISS index is ready for retrieval.")
    print("Run 'python scripts/test_retrieval.py' to test a query.")
    print("=" * 60)


if __name__ == "__main__":
    main()
