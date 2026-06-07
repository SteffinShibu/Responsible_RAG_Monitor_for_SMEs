# Model Card: Responsible RAG Monitor

## Model Overview

| Field | Value |
|---|---|
| **Model name** | BrightPath RAG Assistant |
| **Model type** | Retrieval-Augmented Generation (RAG) |
| **Base LLM** | llama-3.1-8b-instant (via Groq API) |
| **Embedding model** | BAAI/bge-small-en-v1.5 |
| **Evaluator model** | ministral-8b-2512 (via Mistral AI API) |
| **Context window** | 256 tokens per chunk, top-5 chunks retrieved |

## Intended Use

Answer customer support questions using SME internal policy documents. The model is designed to:
- Retrieve relevant policy excerpts from a local vector store
- Generate grounded answers based only on retrieved context
- Recommend escalation when queries exceed the assistant's authority

## Out-of-Scope Use

- Generating answers without retrieved context (hallucination risk)
- Making financial, legal, or HR decisions autonomously
- Processing real customer PII
- Multi-turn conversations (not tested)

## Evaluation Results

See `data/evaluation_results_demo.csv` and `data/evaluation_results.csv` for detailed per-question scores.

Key metrics from the latest evaluation (50 questions):
- Source match rate: ~96%
- Escalation accuracy: ~82%
- Average overall quality: ~0.84 (0-1 scale)

Note: LLM-as-judge scores are directional, not ground truth.

## Known Biases and Limitations

- The underlying LLM (llama-3.1-8b-instant) has its own training data biases
- BGE-small (384-dim) may miss nuanced semantic matches that a larger model would capture
- The golden dataset of 50 questions is synthetic and may not represent real SME query distributions
- The evaluator model (ministral-8b-2512) may have systematic scoring biases

## Monitoring

Statistical process control (SPC) is applied to the overall quality score over the evaluation sequence:
- Shewhart control chart with 3-sigma limits
- Nelson Rule 1: points beyond 3 sigma
- Nelson Rule 2: 9 consecutive points on same side of mean
- Nelson Rule 3: 6 consecutive points increasing or decreasing

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | June 2026 | Initial prototype |
