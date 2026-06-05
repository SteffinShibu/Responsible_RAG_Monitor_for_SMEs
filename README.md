# Responsible RAG Monitor for SMEs

A RAG (Retrieval-Augmented Generation) system for SME policy documents with responsible AI monitoring, built as a portfolio project for responsible AI adoption research.

## Setup

### 1. Clone and prepare environment

```bash
cd responsible-rag-monitor-smes
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows (PowerShell)
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API key (required for Phase 2+)

```bash
cp .env.example .env
```

Then edit `.env` and replace `PASTE_YOUR_GROQ_API_KEY_HERE` with your actual Groq API key.
Get a free key at: https://console.groq.com

---

## Phase 1 — Ingestion & Retrieval Pipeline

Phase 1 builds the core RAG retrieval pipeline: load documents → chunk → embed → FAISS index → query.

### Build the FAISS Index

```bash
python scripts/build_index.py
```

On first run, this downloads the BGE embedding model (~130 MB). Subsequent runs use the cached model.

Expected output:
```
[1/4] Loading documents...
Loaded 10 documents

[2/4] Chunking documents...
Created 111 chunks

[3/4] Embedding chunks with BGE model...
...

[4/4] Building and saving FAISS index...
Index contains 111 vectors with dimension 384
```

### Test a Retrieval Query

```bash
# Single query
python scripts/test_retrieval.py "What is the delivery timeline for Amsterdam?"

# Interactive mode
python scripts/test_retrieval.py
```

---

## Phase 2 — Answer Generation (RAG Pipeline)

Phase 2 connects the retriever to Gemini API so you can ask questions and get natural-language answers based on the policy documents.

### Usage

```bash
# Single question
python scripts/ask_rag.py "What is the standard delivery timeline for Amsterdam?"

# Interactive session
python scripts/ask_rag.py
```

### Example Queries to Try

```bash
python scripts/ask_rag.py "Can AI process refunds over €500?"
python scripts/ask_rag.py "What is the B2B return window?"
python scripts/ask_rag.py "A customer is threatening legal action — what should I do?"
python scripts/ask_rag.py "What happens if tracking says delivered but the customer didn't receive it?"
```

### Expected Answer Format

The answer includes:

- A clear, grounded response based only on policy documents
- `Escalation needed: Yes/No` line
- `Reason:` line explaining the escalation decision
- Sources section listing the relevant documents used

Example output:
```
======================================================================
Q: Can AI process refunds over €500?
======================================================================

--- Answer ---
No, the AI assistant cannot process refunds over €500.00. According
to BrightPath policy, any order with a total value exceeding €500.00
is designated as a "High-Value Transaction." The AI assistant is
strictly prohibited from authorizing refunds, replacements, or
credit notes for these transactions. The request must be escalated
to a Customer Support Supervisor and the Finance Department for
dual sign-off.

Escalation needed: Yes
Reason: The order value exceeds the €500.00 high-value threshold,
which requires supervisor and finance department approval.

--- Sources ---
  [1] refund_and_replacement_policy.md (score: 0.80)
      Title:   BrightPath Office Supplies - Refund and Replacement Policy
      Section: 5. High-Value Order Restrictions
```

### Error Handling

The pipeline handles these errors gracefully:

- **Missing API key**: Clear instructions to set GROQ_API_KEY in `.env`
- **Placeholder key still in `.env`**: Detects unedited placeholder values
- **Empty query**: "Query cannot be empty" message
- **Missing FAISS index**: Instructions to run `build_index.py` first
- **Failed API call**: Error message with details

---

---

## Phase 3 — Streamlit Web App

Phase 3 wraps the RAG pipeline in a simple Streamlit web interface.

### Usage

```bash
streamlit run app/streamlit_app.py
```

This opens a web browser with the RAG assistant interface.

### What the App Demonstrates

- Text input for user questions
- Grounded answer generation using Groq
- Escalation needed Yes/No displayed with color coding
- Expandable sources section showing retrieved chunks with filenames, titles, section headings, scores, and text previews
- Sidebar with system information and sample questions
- Error handling for missing API key, missing FAISS index, and API errors

---

## Project Structure

```
responsible-rag-monitor-smes/
│
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .env                            # Your API key (local only, never committed)
├── .gitignore                      # Git ignore rules
│
├── data/
│   ├── raw_documents/              # 10 SME policy Markdown files
│   └── sample_test_questions.csv   # 50 test questions
│
├── app/
│   └── streamlit_app.py            # Streamlit web app
├── src/
│   ├── config.py                   # Paths, model names, constants
│   ├── utils.py                    # Shared helpers (dependency checks)
│   ├── document_loader.py          # Reads .md files, extracts titles
│   ├── chunker.py                  # Token-based recursive chunking
│   ├── embeddings.py               # BGE model wrapper (sentence-transformers)
│   ├── vector_store.py             # FAISS index build/save/load
│   ├── retriever.py                # Query → top-k relevant chunks
│   ├── generator.py                # Groq wrapper with system prompt
│   └── rag_pipeline.py             # Combines retriever + generator
│
├── scripts/
│   ├── build_index.py              # Build the FAISS index
│   ├── test_retrieval.py           # CLI test: query → raw chunks
│   └── ask_rag.py                  # CLI RAG assistant: query → answer + sources
│
└── vectorstore/
    └── faiss_index/                # Generated: FAISS index + metadata
```

---

## Limitations

- **No RAGAS evaluation** — metrics coming in a later phase
- **No statistical process monitoring** — SPC charts in a later phase
- **No governance artefacts** — system card, model card, risk register in a later phase
- **No chat history persistence** — session resets on page reload
- **Single embedding model** — BGE small (384-dim); BGE base (768-dim) available by changing config
- **Single LLM** — Groq (default: llama-3.1-8b-instant); other providers can be added

---

## What's Next

- RAGAS-style evaluation (faithfulness, answer relevance, context precision)
- LLM-as-judge evaluator rubric
- Statistical process monitoring with Shewhart charts
- Productivity simulation comparing baseline vs AI-assisted
- Governance artefacts (system card, model card, risk register)
