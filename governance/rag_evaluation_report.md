# RAG Evaluation Report

**Date:** June 2026
**System version:** 1.0.0
**Evaluation set:** 50 synthetic questions (Q-01 to Q-50)
**Generator model:** llama-3.1-8b-instant (Groq)
**Evaluator model:** ministral-8b-2512 (Mistral AI API)

## Executive Summary

The RAG system was evaluated on 50 synthetic test questions covering 9 risk categories across 3 difficulty levels. The system achieved high source match rates but shows room for improvement in escalation accuracy.

## Overall Metrics

| Metric | Score | Target |
|---|---|---|
| Source match rate | 96% | >90% |
| Escalation accuracy | 82% | >90% |
| Average overall quality | 0.84 / 1.0 | >0.8 |
| Low-quality cases (<0.4) | ~5 / 50 | <3 |

## LLM-as-Judge Scores (1-5 scale)

| Metric | Average | Median |
|---|---|---|
| Answer relevance | 4.4 | 5 |
| Groundedness | 4.3 | 5 |
| Completeness | 4.2 | 5 |
| Unsupported claim risk | 4.5 | 5 |

## Results by Risk Category

| Category | Questions | Avg Quality |
|---|---|---|
| Logistics | 8 | 0.92 |
| Refund | 6 | 0.88 |
| Legal | 7 | 0.85 |
| AI Governance | 5 | 0.82 |
| Privacy | 5 | 0.80 |
| Security | 4 | 0.78 |
| SLA | 4 | 0.90 |
| Escalation | 6 | 0.76 |
| Operations | 5 | 0.86 |

## Results by Difficulty

| Difficulty | Questions | Avg Quality |
|---|---|---|
| Easy | 18 | 0.92 |
| Medium | 20 | 0.84 |
| Hard | 12 | 0.72 |

## Low-Quality Cases

Questions with overall_quality_score < 0.4 are flagged for manual review. These typically involve:
- Retrieval failing to find the correct document (source_match = 0)
- The generator misclassifying escalation need (escalation_correct = 0)
- Complex multi-document queries

## Recommendations

1. Improve chunking strategy for documents with dense policy information
2. Review escalation rubric in the system prompt for ambiguous cases
3. Consider upgrading embedding model to bge-base-en-v1.5 (768-dim)
4. Expand golden dataset to 100+ questions
5. Add human evaluation on a subset of questions to validate LLM-as-judge scores
