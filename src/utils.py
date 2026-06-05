import sys
from pathlib import Path


def ensure_dir(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def check_path_exists(path: Path, description: str) -> None:
    """Check that a path exists and exit with a clear message if not."""
    if not path.exists():
        print(f"Error: {description} not found at: {path}")
        print("Please check that the path is correct.")
        sys.exit(1)


def check_dependencies():
    """Check that required packages are installed."""
    missing = []
    try:
        import sentence_transformers  # noqa: F401
    except ImportError:
        missing.append("sentence-transformers")
    try:
        import faiss  # noqa: F401
    except ImportError:
        missing.append("faiss-cpu")
    try:
        import tiktoken  # noqa: F401
    except ImportError:
        missing.append("tiktoken")
    try:
        import numpy  # noqa: F401
    except ImportError:
        missing.append("numpy")

    if missing:
        print("Error: missing required dependencies:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nInstall them with:")
        print(f"  pip install {' '.join(missing)}")
        sys.exit(1)
