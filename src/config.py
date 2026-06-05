import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root: two levels up from src/config.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data paths
RAW_DOCUMENTS_DIR = PROJECT_ROOT / "data" / "raw_documents"
TEST_QUESTIONS_PATH = PROJECT_ROOT / "data" / "sample_test_questions.csv"

# Vector store paths
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore" / "faiss_index"
FAISS_INDEX_PATH = VECTORSTORE_DIR / "index.faiss"
METADATA_PATH = VECTORSTORE_DIR / "chunks_metadata.json"

# Embedding model settings
# Switch to "BAAI/bge-base-en-v1.5" for higher accuracy (768-dim)
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
EMBEDDING_DIMENSION = 384  # 768 for bge-base-en-v1.5

# Chunking settings
CHUNK_MAX_TOKENS = 256
CHUNK_OVERLAP_TOKENS = 20

# Retrieval settings
RETRIEVAL_TOP_K = 5

# LLM settings (Groq — OpenAI-compatible API)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
# Best Groq model for RAG: llama-3.3-70b-versatile
# Alternatives: llama-3.3-70b-versatile, mixtral-8x7b-32768
LLM_MODEL_NAME = "llama-3.1-8b-instant"
LLM_TEMPERATURE = 0.1
