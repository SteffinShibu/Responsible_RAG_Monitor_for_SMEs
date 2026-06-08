# V1 Context Handoff — Responsible RAG Monitor for SMEs

> **Generated:** 2026-06-08  
> **Last commit:** `1cd3c54` — Fix evaluator defaults: Mistral primary, Gemini optional fallback  
> **Branch:** `main` — all v1 work is on main  
> **Remote:** `origin` → `https://github.com/SteffinShibu/Responsible_RAG_Monitor_for_SMEs.git`  
> **Deployed app:** https://steffinshibu-responsible-rag-monitor-fo-appstreamlit-app-bmjbbv.streamlit.app/

---

## 1. Core Architecture

### Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Embedding** | `BAAI/bge-small-en-v1.5` (384-dim, sentence-transformers) | Converts document chunks to vectors |
| **Vector store** | FAISS `IndexFlatIP` (inner-product) | Similarity search over chunk embeddings |
| **RAG generator** | Groq API (OpenAI-compatible) → `llama-3.1-8b-instant` | Answer generation from retrieved chunks |
| **LLM-as-judge** | Mistral AI API (OpenAI-compatible) → `ministral-8b-2512` | Evaluation scoring (separate from generator) |
| **Dashboard** | Streamlit + Plotly | App UI + charts |
| **Config** | `.env` / Streamlit secrets via `python-dotenv` + `os.getenv` | API keys, model names, paths |

### Fallback evaluator options
- Mistral (primary): `ministral-8b-2512` via OpenAI-compatible client at `https://api.mistral.ai/v1`
- Gemini (optional): `gemini-1.5-flash-8b` via `google-genai` SDK
- Groq (optional): any Groq-hosted model via OpenAI-compatible client at `https://api.groq.com/openai/v1`

### Data Flow (RAG Pipeline)

```
User Query
  → retriever.retrieve() [BGE embed + FAISS search, top_k=5]
  → chunks + similarity scores
  → generator.generate_answer() [Groq, llama-3.1-8b-instant, temperature=0.1]
  → answer text + escalation decision
  → displayed in Streamlit UI
```

### Data Flow (Evaluation Pipeline)

```
Golden question (50 from sample_test_questions.csv)
  → RAG pipeline → answer + sources
  → rule-based metrics (source_match, escalation_correct)
  → LLM-as-judge (Mistral ministral-8b-2512, temperature=0.0)
  → 4 scores (1-5) + composite overall_quality_score (0-1)
  → appended to evaluation_results.csv
  → Dashboard reads CSV and visualises
```

### Project Structure

```
responsible-rag-monitor-smes/
├── app/streamlit_app.py       # Streamlit app (~725 lines, 2 tabs)
├── src/
│   ├── config.py              # 48 lines — paths, keys, model names, hyperparams
│   ├── utils.py               # dependency & path checks
│   ├── document_loader.py     # load .md files from raw_documents/
│   ├── chunker.py             # token-based recursive chunking (tiktoken)
│   ├── embeddings.py          # BGE embedding via sentence-transformers
│   ├── vector_store.py        # FAISS build/save/load helpers
│   ├── retriever.py           # embed query → FAISS search → return chunks
│   ├── generator.py           # Groq API call + escalation prompt + input validation
│   ├── rag_pipeline.py        # orchestrator: retriever → generator
│   ├── evaluator.py           # 3-backend LLM-as-judge + rule-based metrics
│   ├── evaluation_analysis.py # load/dedup/summarise eval CSV
│   ├── spc_monitor.py         # Shewhart chart + Nelson Rules 1/2/3
│   └── productivity_analysis.py # synthetic productivity comparison
├── scripts/
│   ├── build_index.py         # load → chunk → embed → FAISS save
│   ├── test_retrieval.py      # CLI: query → raw chunks
│   ├── ask_rag.py             # CLI: query → answer + sources
│   └── run_evaluation.py      # batch eval with --resume, --limit, --sleep, --skip-llm-judge
├── data/
│   ├── raw_documents/         # 10 synthetic SME policy .md files
│   ├── sample_test_questions.csv  # 50 golden Qs with expected answers
│   ├── evaluation_results.csv     # gitignored, regenerated per run
│   ├── evaluation_results_demo.csv # committed, fallback for deployment
│   └── synthetic_productivity_data.csv  # 15 scenarios, manual vs AI-assisted
├── governance/                # 8 responsible AI artefact files
│   ├── system_card.md
│   ├── model_card.md
│   ├── rag_evaluation_report.md
│   ├── sme_ai_risk_register.csv
│   ├── incident_log_template.csv
│   ├── human_escalation_checklist.md
│   ├── ai_use_case_taxonomy.csv
│   └── deployment_readiness_checklist.md
├── vectorstore/faiss_index/   # gitignored, auto-built on first Streamlit run
│   ├── index.faiss
│   └── chunks_metadata.json
├── .env.example               # placeholders only, safe to commit
├── .gitignore
├── requirements.txt
├── README.md
├── AGENTS.md                  # (this session) permanent dev rules
└── V1_CONTEXT.md              # ← this file — session handoff
```

---

## 2. Data Schemas & State

### `sample_test_questions.csv` — 50 golden questions

| Column | Type | Notes |
|---|---|---|
| `question_id` | str | `Q-01` through `Q-50` |
| `user_question` | str | The test query text |
| `expected_answer_summary` | str | Ground-truth summary |
| `relevant_document` | str | Filename of expected source doc |
| `risk_category` | str | `Privacy`, `Legal`, `Financial`, `Logistics`, `Operational`, `Ethical`, `Reputational`, `Policy` |
| `should_escalate` | str | `Yes` or `No` |
| `difficulty_level` | str | `Easy`, `Medium`, `Hard` |

### `evaluation_results.csv` — evaluation output (1 row per run per question)

| Column | Type | Source |
|---|---|---|
| `question_id` | str | From test CSV |
| `user_question` | str | From test CSV |
| `expected_answer_summary` | str | From test CSV |
| `relevant_document` | str | From test CSV |
| `risk_category` | str | From test CSV |
| `should_escalate` | str | From test CSV |
| `difficulty_level` | str | From test CSV |
| `generated_answer` | str | RAG output |
| `retrieved_sources` | str | Semicolon-joined `file (score=x.xxxx)` |
| `source_match` | int (0/1) | Rule-based: expected doc found in retrieved? |
| `predicted_escalation` | str | `Yes`/`No`/empty, parsed from answer |
| `escalation_correct` | int (0/1) | Rule-based: prediction matches expected? |
| `answer_relevance_score` | int (1-5) or null | LLM-as-judge |
| `groundedness_score` | int (1-5) or null | LLM-as-judge |
| `completeness_score` | int (1-5) or null | LLM-as-judge |
| `unsupported_claim_risk_score` | int (1-5) or null | LLM-as-judge (5=low risk) |
| `overall_quality_score` | float (0-1) or null | Composite of all metrics above |
| `evaluator_notes` | str | Free-text from judge or error messages |

### `overall_quality_score` formula (in `evaluator.py:compute_overall_quality`)

Average of available components:
- `source_match` (0/1, used as-is)
- `escalation_correct` (0/1, used as-is)
- Each LLM-judge score normalized: `(score - 1) / 4` → clamped `[0, 1]`

If no components available, returns `None`.

### Summary dict (from `evaluation_analysis.py:compute_summary`)

```python
{
    "total_questions": int,
    "source_match_rate": float or None,
    "escalation_accuracy": float or None,
    "avg_overall_quality": float or None,
    "avg_answer_relevance": float or None,
    "avg_groundedness": float or None,
    "avg_completeness": float or None,
    "avg_unsupported_claim_risk": float or None,
    "low_quality_count": int,
    "low_quality_rows": List[Dict],
}
```

### SPC structures (from `spc_monitor.py`)

`compute_control_limits(scores)` → `{"mean", "std", "ucl", "lcl", "n"}`  
→ UCL clipped at 1.0, LCL clipped at 0.0, std uses sample std (n-1).

`get_spc_flags(rows)` → `List[Dict]` each with:
`{"index", "question_id", "user_question", "overall_quality_score", "rule_1_flag", "rule_2_flag", "rule_3_flag", "combined_spc_flag"}`

---

## 3. Implicit Constraints & Design Decisions

### Security & Secrets
- **Never commit `.env`.** It contains real API keys and is in `.gitignore`.
- `data/evaluation_results.csv` is gitignored (regenerated per run).
- `data/evaluation_results_demo.csv` is committed (fallback for deployment — no API keys).
- `vectorstore/faiss_index/*.{faiss,json,pkl}` are gitignored (prevents data leak of embedded document text).
- `.env.example` must contain only placeholder values (`PASTE_YOUR_*_HERE`).
- Streamlit Cloud secrets use exact same key names as `.env` variables.
- The app reads from `os.getenv` — works with both `.env` file and Streamlit secrets.

### Evaluator Model Separation
- The evaluator model is deliberately separate from the generator model to avoid self-evaluation bias.
- Default evaluator is Mistral `ministral-8b-2512` (set in `config.py` line 44-45).
- Gemini is documented as an **optional fallback only** — never the default.
- The `EVALUATOR_PROVIDER` env var controls which backend is used.

### FAISS Index Lifecycle
- FAISS index is NOT committed to git (prevents data leakage of raw document text).
- On first Streamlit startup, `ensure_index_built()` auto-builds the index with a `st.spinner`.
- The builder loads 10 `.md` docs, chunks with tiktoken (256 tokens, 20 overlap), embeds with BGE, saves FAISS.
- If the index exists locally, startup is instant (no rebuild).

### Input Validation
- `generator.py` rejects queries referencing image files (`.png`, `.jpg`, etc.) and other files (`.pdf`, `.docx`, etc.) with a clear error message.
- `generator.py` also catches Groq API errors about unsupported input types and re-raises as `RuntimeError`.

### Chunking Strategy
- Recursive token-based chunking using `tiktoken` (cl100k_base encoding).
- Max tokens per chunk: 256, overlap: 20 tokens.
- Chunks preserve `source_file`, `doc_title`, `section_heading`, and `chunk_id` metadata.

### Escalation Rubric
- The generator's system prompt instructs it to escalate for: transactions >€500, privacy data, legal threats, AI complaints, medical claims, custom pricing, ambiguous policies, or explicit escalation instructions.
- Escalation is detected via `parse_escalation()` which scans for `Escalation needed: Yes/No` in the answer text.

### Streamlit Dashboard Design
- **Tab 1** ("Ask the SME Assistant"): RAG demo with query input, answer display, source expander, sample questions.
- **Tab 2** ("Evaluation Dashboard"): Read-only CSV visualisation — no API calls, loads instantly.
- Dashboard fallback chain: `evaluation_results.csv` → `evaluation_results_demo.csv` → empty state.
- SPC uses question order as a proxy for time (limitation noted in UI).

### Nelson Rules Implemented
- Rule 1: One point beyond 3σ from mean.
- Rule 2: Nine consecutive points on same side of mean.
- Rule 3: Six consecutive points steadily increasing or decreasing.
- Flags are NOT automatic failure labels — displayed as "review by human evaluator" signals.

### Empty / Error States Handled
- `check_prerequisites()` validates GROQ_API_KEY exists and is not a placeholder.
- `ensure_index_built()` builds index if missing, shows spinner, stops if docs missing or chunking fails.
- Dashboard shows `st.info()` with appropriate messages for: no data, missing columns, no quality scores, no risk categories, no difficulty levels, no low-quality cases, no SPC flags.
- Generator returns "no relevant documents" message when retrieval returns empty.
- All evaluator errors are caught and returned as `evaluator_notes` instead of crashing.

### Git Workflow
- All v1 work is on `main` branch (single developer, portfolio project).
- Commit messages are descriptive and reference what changed.
- FAISS index was committed then uncommitted twice during development (final state: not committed).

---

## 4. Active Status

### ✅ Fully Implemented & Working

- [x] **FAISS index build** — 111 chunks from 10 documents, BGE embeddings, IndexFlatIP
- [x] **RAG pipeline** — retrieval + Groq generation with escalation rubric
- [x] **Input validation** — file/image reference rejection in generator
- [x] **Streamlit app Tab 1** — Ask Assistant with sources, escalation display, sample Qs
- [x] **Batch evaluation** — `run_evaluation.py` with `--limit`, `--sleep`, `--resume`, `--skip-llm-judge`
- [x] **Evaluator (3 backends)** — Mistral, Groq, Gemini; all working
- [x] **Evaluation analysis** — load, deduplicate, summarise, group by category/difficulty
- [x] **Evaluation Dashboard (Tab 2)** — KPI cards, 8 chart sections, CSV download
- [x] **SPC monitoring** — Shewhart chart + Nelson Rules 1/2/3
- [x] **Governance artefacts** — 8 files (system card, model card, eval report, risk register, incident log, escalation checklist, use case taxonomy, deployment checklist)
- [x] **Productivity simulation** — synthetic 15-scenario dataset + analysis module
- [x] **Auto-build FAISS at startup** — `ensure_index_built()` in streamlit_app.py
- [x] **Config defaults fixed** — Mistral primary, Gemini optional
- [x] **No data leak** — FAISS index and eval results in `.gitignore`
- [x] **Streamlit Cloud deployment** — app deployed, auto-builds index on first run
- [x] **README.md** — comprehensive docs including architecture, metrics, deployment

### 🟡 Partially Implemented / Known Issues

- [ ] **LLM-as-judge failure rate** — 15/50 Mistral API failures in the last full run (likely Mistral API rate limits or transient errors; check `evaluator_notes` column in CSV for details).
- [ ] **Copy-paste blocked in Streamlit** — `Cmd+C` triggers "Clear cache" by default; a JS workaround was discussed but not fully tested.
- [ ] **torchvision warnings** — Harmless `ModuleNotFoundError: No module named 'torchvision'` warnings flood Streamlit logs (from `transformers` package introspection), not affecting function.
- [ ] **use_container_width deprecation** — Streamlit warns `use_container_width` will be removed after 2025-12-31; should use `width='stretch'` instead.
- [ ] **STREAMLIT_ROBOT_FILE env var** — App prints `STREAMLIT_ROBOT_FILE` warning; cosmetic only.

### ❌ Not Started / Planned for V2

- [ ] **Human evaluation layer** — Validate LLM-as-judge scores against human raters
- [ ] **Live telemetry** — Time-series SPC monitoring from real user-query logs (not static benchmark)
- [ ] **Expanded golden dataset** — 200+ questions (currently 50)
- [ ] **Multi-turn conversation** — Chat history persistence
- [ ] **Authentication & access control** — For deployment beyond demo
- [ ] **Privacy impact assessment** — Full DPIA documentation
- [ ] **Governance dashboard** — Dedicated tab for risk register, incident log, compliance status
- [ ] **Field productivity study** — Real intervention (not synthetic) with difference-in-differences analysis

---

## 5. V2 Immediate Next Steps

### Priority 1: Fix Streamlit copy-paste
Add `<script>` to intercept `Cmd+C` before Streamlit's cache-clear handler fires.

### Priority 2: Fix use_container_width deprecation
Replace `use_container_width=True` with `width='stretch'` in all Streamlit widgets.

### Priority 3: Reduce LLM-as-judge failures
Investigate Mistral API 15/50 failure rate. Options:
- Add retry logic in `judge_answer()`
- Increase API request timeout
- Switch to Gemini or Groq as fallback on failure
- Check `evaluator_notes` for specific error patterns

### Priority 4: Governance dashboard tab
Create a third Streamlit tab that renders risk register, incident log, and deployment checklist from `governance/` artefacts.

### Priority 5: Live SPC monitoring
- Add a timestamp column to evaluation results
- Stream real user queries into evaluation loop
- Replace question-order proxy with actual time series

---

## 6. Environment Variables Reference

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `GROQ_API_KEY` | **Yes** | `""` | Answer generator API key |
| `LLM_PROVIDER` | No | `"groq"` | Generator provider (currently only groq supported) |
| `LLM_MODEL_NAME` | No | `"llama-3.1-8b-instant"` | Generator model |
| `MISTRAL_API_KEY` | For Mistral evaluator | `""` | Evaluator API key (Mistral) |
| `GEMINI_API_KEY` | For Gemini evaluator | `""` | Evaluator API key (Gemini, optional fallback) |
| `EVALUATOR_PROVIDER` | No | `"mistral"` | Evaluator backend: `mistral`, `groq`, or `gemini` |
| `EVALUATOR_MODEL_NAME` | No | `"ministral-8b-2512"` | Evaluator model name |
| `EMBEDDING_MODEL` | No | `"BAAI/bge-small-en-v1.5"` | Embedding model HF path |

---

## 7. Commands Reference

```bash
# Build FAISS index
python scripts/build_index.py

# Run RAG assistant (CLI)
python scripts/ask_rag.py "your question"

# Run evaluation
python scripts/run_evaluation.py --limit 5 --sleep 2 --skip-llm-judge  # quick
python scripts/run_evaluation.py --sleep 10                            # full

# Resume evaluation (skips already-processed Qs)
python scripts/run_evaluation.py --resume --sleep 15

# Launch Streamlit app
streamlit run app/streamlit_app.py

# Productivity analysis
python src/productivity_analysis.py
```

---

## 8. Deployment Checklist

### Streamlit Cloud secrets (must set in Settings → Secrets):
```toml
GROQ_API_KEY = "your_groq_api_key_here"
LLM_PROVIDER = "groq"
LLM_MODEL_NAME = "llama-3.1-8b-instant"
MISTRAL_API_KEY = "your_mistral_api_key_here"
EVALUATOR_PROVIDER = "mistral"
EVALUATOR_MODEL_NAME = "ministral-8b-2512"
```

### Verification after redeploy:
1. Sidebar shows: Provider `mistral`, Judge model `ministral-8b-2512`
2. Status box says "SPC monitoring" under current capabilities
3. Evaluation Dashboard loads charts
4. SPC title includes "over RAG Evaluation Scores"
5. No Gemini references in sidebar or status
6. No API keys or local paths visible
