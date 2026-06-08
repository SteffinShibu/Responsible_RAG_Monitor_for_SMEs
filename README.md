# Responsible RAG Monitor for SMEs

A responsible AI evaluation and monitoring toolkit for SME retrieval-augmented generation (RAG) systems. Built as a portfolio project for UvA's _AI for All_ PhD programme.

> **This is not just a chatbot.** The RAG assistant is the user-facing test system. The main contribution is the evaluation, monitoring, and governance layer around it.

---

## Live Demo

**Streamlit app:** [https://steffinshibu-responsible-rag-monitor-fo-appstreamlit-app-bmjbbv.streamlit.app/](https://steffinshibu-responsible-rag-monitor-fo-appstreamlit-app-bmjbbv.streamlit.app/)

---

## Why This Matters

Small and medium-sized enterprises (SMEs) increasingly adopt AI assistants for customer support, but lack the resources to evaluate and monitor these systems for responsible AI behaviour. This project demonstrates a practical V1 toolkit for:

- **Evaluating** RAG answer quality using both rule-based metrics and a separate LLM-as-judge
- **Monitoring** quality over time with statistical process control (SPC) charts and Nelson rule detection
- **Governing** AI use through system cards, model cards, risk registers, and escalation processes

---

## Project Structure

```
responsible-rag-monitor-smes/
│
├── app/
│   └── streamlit_app.py              # Streamlit app (Ask Assistant + Evaluation Dashboard)
│
├── src/
│   ├── config.py                     # Paths, model names, API keys, constants
│   ├── utils.py                      # Dependency and path checks
│   ├── document_loader.py            # Read .md files, extract titles
│   ├── chunker.py                    # Token-based recursive chunking (tiktoken)
│   ├── embeddings.py                 # BGE embedding model (sentence-transformers)
│   ├── vector_store.py               # FAISS index build/save/load
│   ├── retriever.py                  # Top-k retrieval with relevance scores
│   ├── generator.py                  # Groq API wrapper with escalation system prompt
│   ├── rag_pipeline.py               # Combines retriever + generator
│   ├── evaluator.py                  # LLM-as-judge (Mistral, Groq, or Gemini) + rule-based metrics
│   ├── evaluation_analysis.py        # Load, deduplicate, summarise evaluation results
│   ├── spc_monitor.py                # Shewhart SPC charts + Nelson rules
│   └── productivity_analysis.py      # Lightweight productivity comparison
│
├── scripts/
│   ├── build_index.py                # Build the FAISS index
│   ├── test_retrieval.py             # CLI test: query → raw chunks
│   ├── ask_rag.py                    # CLI RAG assistant: query → answer + sources
│   └── run_evaluation.py             # Batch evaluation against golden dataset
│
├── data/
│   ├── raw_documents/                # 10 synthetic SME policy documents (.md)
│   ├── sample_test_questions.csv     # 50 golden test questions with expected answers
│   ├── evaluation_results_demo.csv   # Demo evaluation results (committed for deployment)
│   ├── evaluation_results.csv        # Local evaluation results (gitignored, regenerated)
│   └── synthetic_productivity_data.csv  # Synthetic productivity comparison data
│
├── governance/
│   ├── system_card.md                # System overview and component descriptions
│   ├── model_card.md                 # Model details, biases, and evaluation results
│   ├── rag_evaluation_report.md      # Evaluation findings and recommendations
│   ├── sme_ai_risk_register.csv      # AI risk identification and mitigation
│   ├── incident_log_template.csv     # Incident tracking template
│   ├── human_escalation_checklist.md # Escalation handling procedure
│   ├── ai_use_case_taxonomy.csv      # SME AI use case classification
│   └── deployment_readiness_checklist.md  # Deployment preparation steps
│
├── vectorstore/
│   └── faiss_index/                  # Generated FAISS index + metadata (not committed)
│
├── .env.example                      # Environment variable template (placeholders only)
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

---

## Architecture

```
User Query
    │
    ▼
┌─────────────────────┐
│   Retriever         │
│   (BGE embeddings   │
│    + FAISS search)  │
└─────────┬───────────┘
          │  top-5 chunks + scores
          ▼
┌─────────────────────┐
│   Generator         │
│   (Groq /           │
│    llama-3.1-8b)    │
└─────────┬───────────┘
          │  grounded answer + escalation decision
          ▼
┌─────────────────────┐      ┌──────────────────────┐
│   RAG Assistant     │      │  Evaluator            │
│   (user-facing demo)│─────▶│  (Mistral LLM-as-judge│
│                     │      │   as judge)           │
└─────────────────────┘      └──────────┬───────────┘
                                        │ scores + flags
                                        ▼
                               ┌──────────────────────┐
                               │  Dashboard + SPC     │
                               │  (Streamlit + plotly) │
                               └──────────────────────┘
```

The evaluator model is used as a secondary review layer to assess answer quality, safety, and escalation behaviour. It is not treated as ground truth; its outputs are compared against a small golden dataset and monitored over time.

---

## Quick Start

### 1. Prerequisites

- Python 3.10+
- Groq API key (free at [console.groq.com](https://console.groq.com))
- Mistral AI API key (free at [console.mistral.ai](https://console.mistral.ai)) — for LLM-as-judge
  Or Gemini API key (free at [aistudio.google.com](https://aistudio.google.com/apikey)) — optional alternative

### 2. Setup

```bash
git clone https://github.com/SteffinShibu/Responsible_RAG_Monitor_for_SMEs.git
cd responsible-rag-monitor-smes
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your API keys.

### 3. Build the index

```bash
python scripts/build_index.py
```

### 4. Run the RAG assistant

**CLI:**
```bash
python scripts/ask_rag.py "What is the delivery timeline for Amsterdam?"
```

**Streamlit app:**
```bash
streamlit run app/streamlit_app.py
```

### 5. Run evaluation

```bash
# Quick test (5 questions, rule-based only)
python scripts/run_evaluation.py --limit 5 --sleep 2 --skip-llm-judge

# Full evaluation with LLM-as-judge
python scripts/run_evaluation.py --sleep 15
```

---

## Streamlit Dashboard

The app has two tabs:

### Ask the SME Assistant

The user-facing RAG demo. Ask questions about BrightPath Office Supplies' internal policies. The assistant:
- Retrieves relevant policy chunks from the FAISS vector store
- Generates a grounded answer using Groq
- Includes source citations with similarity scores
- Recommends escalation when appropriate (high-value transactions, legal threats, privacy issues, etc.)

### Evaluation Dashboard

Visualises results from the evaluation module. Shows:
- **KPI cards**: questions evaluated, average quality, source match rate, escalation accuracy, LLM-judge metric averages
- **Score distribution**: histogram of overall quality scores
- **Metric averages**: bar chart of LLM-as-judge scores
- **Risk category breakdown**: quality by category with question counts
- **Difficulty breakdown**: quality by difficulty level
- **Detail tables**: low-quality cases, failed escalation, failed source match
- **CSV download**: export deduplicated evaluation results
- **SPC chart**: Shewhart control chart with Nelson rule flags

---

## Evaluation Metrics

| Metric | Type | Range | Description |
|---|---|---|---|
| `source_match` | Rule-based | 0 or 1 | Did the retriever find the expected document? |
| `escalation_correct` | Rule-based | 0 or 1 | Did the assistant correctly escalate? |
| `answer_relevance_score` | LLM-judge | 1-5 | Does the answer address the question? |
| `groundedness_score` | LLM-judge | 1-5 | Are claims supported by context? |
| `completeness_score` | LLM-judge | 1-5 | Does it cover expected information? |
| `unsupported_claim_risk_score` | LLM-judge | 1-5 | Risk from unsupported claims (5 = low risk) |
| `overall_quality_score` | Composite | 0-1 | Weighted average of all metrics |

---

## Statistical Process Control (SPC)

### Shewhart Control Chart

The dashboard plots `overall_quality_score` as a run chart over the evaluation sequence with:
- **Centre line**: mean quality score
- **UCL**: mean + 3σ (clipped at 1.0)
- **LCL**: mean − 3σ (clipped at 0.0)
- Highlighted low-quality points (score < 0.4)

### Nelson Rules

| Rule | Description |
|---|---|
| Rule 1 | One point beyond 3 standard deviations from the mean |
| Rule 2 | Nine consecutive points on the same side of the mean |
| Rule 3 | Six consecutive points steadily increasing or decreasing |

**Note:** In V1, question order from the evaluation sequence is used as a proxy for time. In production, SPC would run over timestamped real user queries.

---

## Governance Artefacts

The `governance/` folder contains:

| File | Purpose |
|---|---|
| `system_card.md` | System architecture, components, intended use, limitations |
| `model_card.md` | Model details, biases, evaluation results, version history |
| `rag_evaluation_report.md` | Detailed evaluation findings and recommendations |
| `sme_ai_risk_register.csv` | 8 identified AI risks with likelihood, impact, and mitigations |
| `incident_log_template.csv` | Template for logging AI incidents |
| `human_escalation_checklist.md` | Step-by-step escalation handling guide |
| `ai_use_case_taxonomy.csv` | 8 SME AI use cases with risk levels and oversight requirements |
| `deployment_readiness_checklist.md` | Deployment preparation and production considerations |

---

## Productivity Simulation

Synthetic productivity data (`data/synthetic_productivity_data.csv`) compares manual vs AI-assisted support for 15 scenarios. Analysis shows:

| Metric | Manual | AI-Assisted |
|---|---|---|
| Avg resolution time | 22.8 min | 6.6 min |
| Error rate | 53% | 13% |
| Time savings | — | 71% |

**Note:** This uses synthetic data to demonstrate how a productivity evaluation could be structured. Real deployment would require field intervention with proper controls (difference-in-differences, panel analysis, etc.).

---

## Deploy on Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select the repo and set main file to `app/streamlit_app.py`
4. Add these secrets in Streamlit Cloud dashboard → Settings → Secrets:

```toml
GROQ_API_KEY = "your_groq_api_key"
MISTRAL_API_KEY = "your_mistral_api_key"
EVALUATOR_PROVIDER = "mistral"
EVALUATOR_MODEL_NAME = "ministral-8b-2512"
```

The dashboard works without API keys for visualising existing evaluation results.

---

## Limitations

- **Synthetic data only**: Documents and test questions are artificial — not validated on real SME data
- **LLM-as-judge is not ground truth**: Scores are directional and may contain systematic biases
- **Static benchmark**: V1 evaluates a fixed set of 50 questions, not live user traffic
- **Small evaluation set**: 50 questions may not represent real-world query distribution
- **Single embedding model**: BGE-small (384-dim); upgrading to bge-base-en-v1.5 (768-dim) may improve retrieval
- **No multi-turn**: The assistant handles single questions only
- **No chat persistence**: Session resets on page reload

---

## V2 Roadmap

- Human evaluation layer to validate LLM-as-judge scores
- Live telemetry and time-series SPC monitoring
- Expanded golden dataset (200+ questions)
- Multi-turn conversation support
- Chat history persistence
- Privacy impact assessment
- Authentication and access control
- Integration with real SME policy documents (anonymised)

---

## License

Portfolio project for educational and research purposes only. Not for production use.
