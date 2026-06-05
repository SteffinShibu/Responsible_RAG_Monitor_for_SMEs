"""
Command-line test script for Phase 1 retrieval.

Usage:
    python scripts/test_retrieval.py "your query here"

Examples:
    python scripts/test_retrieval.py "What is the standard delivery timeline for Amsterdam?"
    python scripts/test_retrieval.py "Can I return a €600 desk?"
    python scripts/test_retrieval.py "What is the process for a GDPR data deletion request?"

If no query is provided, the script runs an interactive loop where
you can type queries repeatedly.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.utils import check_dependencies
from src.retriever import retrieve


def display_results(query: str, results: list):
    """Pretty-print retrieval results to the console."""
    print("\n" + "=" * 70)
    print(f"Query: {query}")
    print("=" * 70)

    if not results:
        print("No results found.")
        return

    for i, r in enumerate(results, 1):
        print(f"\n--- Result {i} (score: {r['similarity_score']}) ---")
        print(f"  Source file:     {r['source_file']}")
        print(f"  Document title:  {r['doc_title']}")
        print(f"  Section heading: {r['section_heading']}")
        print(f"  Chunk ID:        {r['chunk_id']}")
        print(f"  Text:")
        print(f"    {r['text'][:300]}..." if len(r['text']) > 300 else f"    {r['text']}")
        print()

    # Summary stats
    scores = [r["similarity_score"] for r in results]
    print(f"Score range: {min(scores):.4f} – {max(scores):.4f}")


def main():
    check_dependencies()

    if len(sys.argv) > 1:
        # Single query from command line
        query = " ".join(sys.argv[1:])
        try:
            results = retrieve(query)
            display_results(query, results)
        except RuntimeError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        print("Interactive Retrieval Test")
        print("Type 'exit' or 'quit' to stop.")
        print()
        while True:
            try:
                query = input("Enter your query: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if query.lower() in ("exit", "quit", ""):
                break
            try:
                results = retrieve(query)
                display_results(query, results)
            except RuntimeError as e:
                print(f"Error: {e}")
                break


if __name__ == "__main__":
    main()
