"""
Command-line RAG assistant for Phase 2.

Usage:
    python scripts/ask_rag.py "your question here"

Examples:
    python scripts/ask_rag.py "What is the standard delivery timeline for Amsterdam?"
    python scripts/ask_rag.py "Can AI process refunds over €500?"
    python scripts/ask_rag.py "What is the process for a GDPR data deletion request?"

If no query is provided, the script runs an interactive session where
you can type questions repeatedly.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.utils import check_dependencies
from src.rag_pipeline import answer_query


MAX_PREVIEW_LENGTH = 200


def display_answer(result: dict):
    """Pretty-print the RAG answer and sources to the console."""
    query = result["query"]
    answer = result["answer"]
    sources = result["sources"]

    print("\n" + "=" * 70)
    print(f"Q: {query}")
    print("=" * 70)

    print("\n--- Answer ---")
    print(answer)

    if sources:
        print("\n--- Sources ---")
        for i, s in enumerate(sources, 1):
            print(f"\n  [{i}] {s['source_file']} (score: {s['similarity_score']})")
            print(f"      Title:   {s['doc_title']}")
            print(f"      Section: {s['section_heading']}")
            text = s['text']
            preview = text[:MAX_PREVIEW_LENGTH] + "..." if len(text) > MAX_PREVIEW_LENGTH else text
            print(f"      Preview: {preview}")
    else:
        print("\n(No sources were retrieved for this query.)")

    print()


def main():
    check_dependencies()

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        try:
            result = answer_query(query)
            display_answer(result)
        except (ValueError, RuntimeError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)
    else:
        print("Responsible RAG Assistant — Interactive Mode")
        print("Type 'exit' or 'quit' to stop.")
        print()
        while True:
            try:
                query = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if query.lower() in ("exit", "quit", ""):
                break
            try:
                result = answer_query(query)
                display_answer(result)
            except (ValueError, RuntimeError) as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    print("Goodbye!")


if __name__ == "__main__":
    main()
