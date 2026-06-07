# System Card: Responsible RAG Monitor for SMEs

## System Overview

| Field | Value |
|---|---|
| **System name** | Responsible RAG Monitor for SMEs |
| **Version** | 1.0.0 (prototype) |
| **Date** | June 2026 |
| **Status** | Research prototype — not for production use |

## Purpose

A retrieval-augmented generation (RAG) system that answers customer support questions using SME internal policy documents, with a built-in responsible AI evaluation and monitoring layer. The system is designed as a testbed for studying responsible AI adoption in small and medium-sized enterprises (SMEs).

## Intended Users

- SME customer support agents (as end users of the RAG assistant)
- SME compliance officers (reviewing escalation and safety metrics)
- AI adoption researchers (evaluating system behaviour over time)

## Out-of-Scope Uses

- Real customer support without human oversight
- Legal, financial, or HR decision-making
- Processing of personally identifiable information (PII) in production
- Automated refund or compensation approvals
- Use as a replacement for human judgement in escalated cases

## Components

| Component | Technology | Purpose |
|---|---|---|
| Document loader | Custom (Python) | Reads `.md` policy files, extracts titles and sections |
| Chunker | Custom (tiktoken) | Token-based recursive chunking (256 tokens, 20-token overlap) |
| Embedding model | BAAI/bge-small-en-v1.5 (384-dim) | Converts chunks to vector embeddings |
| Vector store | FAISS (IndexFlatIP) | Similarity search over embedded chunks |
| Retrieval | Custom | Top-k retrieval with relevance scores |
| Answer generator | Groq (llama-3.1-8b-instant) | Generates grounded answers from retrieved context |
| LLM-as-judge | Mistral (ministral-8b-2512) via Mistral AI API | Evaluates answer quality and safety |
| Dashboard | Streamlit | Interactive visualisation and SPC monitoring |
| SPC monitor | Custom (Python) | Shewhart control charts and Nelson rule detection |

## Data Sources

- 10 synthetic Markdown policy documents for a fictional SME (BrightPath Office Supplies)
- 50 synthetic test questions with expected answers and escalation labels
- All data is synthetic — no real customer data, PII, or business secrets

## Evaluation Method

The evaluator model is used as a secondary review layer to assess answer quality, safety, and escalation behaviour. It is not treated as ground truth; its outputs are compared against a small golden dataset and monitored over time.

Metrics:
- **Rule-based**: source_match, escalation_correct
- **LLM-as-judge (1-5)**: answer_relevance, groundedness, completeness, unsupported_claim_risk
- **Composite**: overall_quality_score (0-1)

## Known Limitations

- Synthetic documents and questions only — not validated on real SME data
- LLM-as-judge is a proxy, not human evaluation
- Static benchmark, not live telemetry
- 50-question dataset is small and may not generalise
- Single embedding model (BGE small); dimension 384 may limit retrieval quality
- No multi-turn conversation support
- No persistent chat history

## Human Oversight

- All escalated questions are flagged for human review
- Low-quality answers (score < 0.4) are flagged for human audit
- SPC flags trigger review, not automatic actions
- Escalation checklist is provided for human agents

## Privacy and Sensitive-Data Risks

- The system should not be used with real PII in production without privacy impact assessment
- The current prototype uses only synthetic data
- No data is logged or stored by the LLM provider beyond the API call
- Users should not paste customer PII into the assistant
