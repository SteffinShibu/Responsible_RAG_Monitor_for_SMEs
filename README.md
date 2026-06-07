# Responsible RAG Monitor for SMEs

A RAG (Retrieval-Augmented Generation) system for SME policy documents with responsible AI monitoring, built as a portfolio project for responsible AI adoption research.

## Live Demo

**Streamlit app:** https://steffinshibu-responsible-rag-monitor-fo-appstreamlit-app-bmjbbv.streamlit.app/

This deployed V1 currently demonstrates the user-facing RAG assistant module. Later phases will add RAGAS-style evaluation, LLM-as-judge scoring, statistical process monitoring, productivity simulation, and governance artefacts.

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

## Phase 4 — Batch Evaluation Module (RAGAS-style)

Phase 4 evaluates the RAG system against the 50-question golden dataset using a combination of rule-based metrics and a separate LLM-as-judge.

### Architecture

- **Answer generator:** Groq (`llama-3.1-8b-instant`) — same model used in the RAG pipeline
- **Evaluator/judge:** Gemini (`gemini-1.5-flash-8b`) — a separate model, never the same as the generator

Using a separate model for evaluation avoids self-evaluation bias. The judge never sees its own answers.

### Metrics

| Metric | Type | Description |
|---|---|---|
| `source_match` | Rule-based (1/0) | 1 if the expected document appears in retrieved sources |
| `escalation_correct` | Rule-based (1/0) | 1 if the answer's "Escalation needed" matches expected |
| `answer_relevance_score` | LLM-judge (1-5) | Does the answer directly address the question? |
| `groundedness_score` | LLM-judge (1-5) | Are all claims supported by retrieved context? |
| `completeness_score` | LLM-judge (1-5) | Does the answer cover the expected information? |
| `unsupported_claim_risk_score` | LLM-judge (1-5) | How much risk from unsupported claims? (5 = low risk) |
| `overall_quality_score` | Composite (0-1) | Weighted average of all the above metrics |

### Usage

**Small test run (5 questions, 10s between questions):**
```bash
python scripts/run_evaluation.py --limit 5 --sleep 10
```

**Resume from where you left off:**
```bash
python scripts/run_evaluation.py --resume --limit 5 --sleep 10
```

**Start from a specific row index:**
```bash
python scripts/run_evaluation.py --start 10 --limit 5 --sleep 10
```

**Retrieval-only evaluation (no LLM judge calls):**
```bash
python scripts/run_evaluation.py --limit 5 --skip-llm-judge
```

**Full evaluation (when rate limits allow):**
```bash
python scripts/run_evaluation.py --sleep 15
```

### Rate-Limit Safety

Both Groq and Gemini free tiers have rate limits. The evaluation script is designed to work within these constraints:

- Results are saved **after each question**, not only at the end
- `--sleep` controls the delay between questions (default: 10 seconds)
- `--limit` controls how many questions are processed in one run
- `--start` skips to a specific row index
- `--resume` skips question_ids already in the results CSV
- If a rate-limit error occurs, progress is saved and the script stops gracefully

### Results Format

Results are saved to `data/evaluation_results.csv` with these columns:

- `question_id`, `user_question`, `expected_answer_summary`
- `relevant_document`, `risk_category`, `should_escalate`, `difficulty_level`
- `generated_answer` — the full RAG-generated answer
- `retrieved_sources` — source filenames with similarity scores
- `source_match` — 0 or 1
- `predicted_escalation` — "yes" / "no" parsed from the answer
- `escalation_correct` — 0 or 1
- `answer_relevance_score`, `groundedness_score`, `completeness_score`, `unsupported_claim_risk_score` — 1-5 or blank
- `overall_quality_score` — 0-1 composite
- `evaluator_notes` — judge comments or error descriptions

### Interpreting the Results

- **source_match** below 0.7 suggests the retriever is missing the right document
- **escalation_correct** below 0.8 suggests the generator is not following the escalation rubric
- **answer_relevance** below 3 indicates the answer misses the question
- **groundedness** below 3 suggests hallucination or unsupported claims
- **unsupported_claim_risk_score** below 3 is a red flag for responsible AI
- **overall_quality_score** below 0.4 flags a problematic case
- LLM-as-judge scores can vary by run — treat as directional, not absolute

### Limitations

- LLM-as-judge is not perfect: the judge may miss subtle errors or be overly strict
- The judge prompt and rubric influence scores significantly
- Rule-based escalation parsing depends on the generator including the "Escalation needed:" line
- source_match checks filename substring matching, which may over-match on similar filenames
- 50 questions is a small evaluation set — results may not generalise

---

## Phase 5 — Evaluation Dashboard & Statistical Process Monitoring

Phase 5 adds an interactive Streamlit dashboard to visualise evaluation results and monitor system quality with statistical process control (SPC) charts.

### Architecture

The dashboard reads from `data/evaluation_results.csv` (generated by Phase 4). It does **not** call any LLM API — no Groq, no Gemini, no Mistral. This means the dashboard loads instantly and works offline.

Two new modules are added:

| Module | Purpose |
|---|---|
| `src/evaluation_analysis.py` | Load, deduplicate, summarise, and group evaluation results |
| `src/spc_monitor.py` | Compute Shewhart control limits and detect Nelson Rule violations |

### Dashboard Sections

**Key Metrics (KPI cards):**
- Total questions evaluated
- Average overall quality score
- Source match rate (%)
- Escalation accuracy (%)
- All four LLM-as-judge metric averages (relevance, groundedness, completeness, unsupported claim risk)
- Count of low-quality cases (score < 0.4)

**Charts and Tables:**

| Section | Type | What it shows |
|---|---|---|
| A. Score Distribution | Histogram | Distribution of overall_quality_score values |
| B. Metric Averages | Bar chart | Average of all 4 LLM-judge metrics (1-5 scale) |
| C. Results by Risk Category | Bar chart | Average quality score per risk category with question count |
| D. Results by Difficulty | Bar chart | Average quality score per difficulty level with question count |
| E. Source Match & Escalation | Bar chart | Percentage rates for both rule-based metrics |
| F. Low-Quality Cases | Table | All rows where overall_quality_score < 0.4 |
| G. Failed Escalation | Table | All rows where escalation_correct == 0 |
| H. Failed Source Match | Table | All rows where source_match == 0 |

**Statistical Process Control (SPC):**

**Shewhart Control Chart** — Shows overall_quality_score as a run chart with:
- Centre line (mean)
- Upper control limit (UCL = mean + 3σ)
- Lower control limit (LCL = mean − 3σ, clipped at 0)
- Highlighted low-quality points (score < 0.4)
- Hover tooltip with exact values

**Nelson Rules Implemented:**

| Rule | Description |
|---|---|
| Rule 1 | One point beyond 3 standard deviations from the mean |
| Rule 2 | Nine consecutive points on the same side of the mean |
| Rule 3 | Six consecutive points steadily increasing or decreasing |

Flagged points are shown in a table below the chart with the specific rules triggered.

**CSV Download:**
A download button lets you export the deduplicated evaluation results.

### How to Run

```bash
# First, ensure evaluation results exist
python scripts/run_evaluation.py --limit 5 --sleep 10

# Then launch the dashboard
streamlit run app/streamlit_app.py
```

The app opens in your browser with two tabs: **Ask the SME Assistant** (the RAG demo) and **Evaluation Dashboard** (Phase 5).

### How to Interpret the Dashboard

- **Source match** measures whether retrieval found the expected document. Below 70% suggests the retriever or chunking strategy needs improvement.
- **Escalation accuracy** measures whether the assistant correctly recommended human review. Below 80% suggests the generator is not following the escalation rubric consistently.
- **LLM-as-judge scores** are model-based evaluation proxies, not ground truth. They provide directional quality signals.
- **SPC flags** are monitoring signals that indicate unusual patterns. They should trigger human review, not automatic conclusions.
- **Low-quality cases** (score < 0.4) are candidates for manual review and system improvement.

### Limitations

- This is a **static benchmark**, not live monitoring. Question order is used as a proxy sequence for SPC.
- LLM-as-judge scores reflect the specific judge model and prompt used — scores will vary with different judges.
- The 50-question dataset is synthetic and may not represent real-world query distribution.
- SPC with a small sample (50 points) has wide control limits — more data improves sensitivity.

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
│   ├── sample_test_questions.csv   # 50 test questions
│   └── evaluation_results.csv      # Generated evaluation results
│
├── app/
│   └── streamlit_app.py            # Streamlit web app (Ask Assistant + Evaluation Dashboard)
├── src/
│   ├── config.py                   # Paths, model names, constants
│   ├── utils.py                    # Shared helpers (dependency checks)
│   ├── document_loader.py          # Reads .md files, extracts titles
│   ├── chunker.py                  # Token-based recursive chunking
│   ├── embeddings.py               # BGE model wrapper (sentence-transformers)
│   ├── vector_store.py             # FAISS index build/save/load
│   ├── retriever.py                # Query → top-k relevant chunks
│   ├── generator.py                # Groq wrapper with system prompt
│   ├── rag_pipeline.py             # Combines retriever + generator
│   ├── evaluator.py                # LLM-as-judge (Gemini or Groq/Mistral) + rule-based metrics
│   ├── evaluation_analysis.py      # Phase 5: load, dedup, summarise, group results
│   └── spc_monitor.py              # Phase 5: Shewhart SPC + Nelson rules
│
├── scripts/
│   ├── build_index.py              # Build the FAISS index
│   ├── test_retrieval.py           # CLI test: query → raw chunks
│   ├── ask_rag.py                  # CLI RAG assistant: query → answer + sources
│   └── run_evaluation.py           # Batch evaluation against golden dataset
│
└── vectorstore/
    └── faiss_index/                # Generated: FAISS index + metadata
```

---

## Limitations

- **No productivity simulation** — baseline comparison in a later phase
- **No governance dashboard** — system card, model card, risk register in a later phase
- **No chat history persistence** — session resets on page reload
- **Single embedding model** — BGE small (384-dim); BGE base (768-dim) available by changing config
- **LLM-as-judge is not perfect** — scores are directional, not absolute
- **50 questions is a small evaluation set** — results may not generalise
- **Static benchmark, not live monitoring** — SPC uses question order as proxy for time

---

## What's Next

- Productivity simulation comparing baseline vs AI-assisted
- Governance artefacts (system card, model card, risk register)
