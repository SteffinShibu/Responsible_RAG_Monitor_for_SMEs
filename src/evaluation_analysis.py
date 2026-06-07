"""
Helper functions for loading, deduplicating, and analysing evaluation results.

Designed to be used by both the Streamlit dashboard and CLI analysis scripts.
"""

import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from src.config import EVALUATION_RESULTS_PATH

EXPECTED_COLUMNS = [
    "question_id",
    "user_question",
    "expected_answer_summary",
    "relevant_document",
    "risk_category",
    "should_escalate",
    "difficulty_level",
    "generated_answer",
    "retrieved_sources",
    "source_match",
    "predicted_escalation",
    "escalation_correct",
    "answer_relevance_score",
    "groundedness_score",
    "completeness_score",
    "unsupported_claim_risk_score",
    "overall_quality_score",
    "evaluator_notes",
]

NUMERIC_COLS = [
    "source_match",
    "escalation_correct",
    "answer_relevance_score",
    "groundedness_score",
    "completeness_score",
    "unsupported_claim_risk_score",
    "overall_quality_score",
]


def load_results(path: Optional[Path] = None) -> List[Dict]:
    """Load evaluation results CSV. Returns empty list if file missing."""
    p = path or EVALUATION_RESULTS_PATH
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def deduplicate_rows(rows: List[Dict]) -> List[Dict]:
    """
    Deduplicate by question_id, keeping the latest row for each.
    Assumes rows are in chronological order (first = oldest, last = newest).
    """
    seen = {}
    for row in rows:
        qid = row.get("question_id", "").strip()
        if qid:
            seen[qid] = row
    return list(seen.values())


def validate_columns(rows: List[Dict]) -> List[str]:
    """Return a list of missing column names. Empty list means all OK."""
    if not rows:
        return []
    missing = []
    for col in EXPECTED_COLUMNS:
        if col not in rows[0]:
            missing.append(col)
    return missing


def safe_float(val, default=None) -> Optional[float]:
    """Convert a value to float safely. Handles empty strings, None, etc."""
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return float(val)
    stripped = str(val).strip()
    if not stripped:
        return default
    try:
        return float(stripped)
    except (ValueError, TypeError):
        return default


def compute_summary(rows: List[Dict]) -> Dict:
    """
    Compute summary metrics from deduplicated rows.
    Returns a dict with keys for each metric.
    """
    n = len(rows)

    source_match_vals = [safe_float(r.get("source_match")) for r in rows]
    source_match_vals = [v for v in source_match_vals if v is not None]
    source_match_rate = sum(source_match_vals) / len(source_match_vals) if source_match_vals else None

    escalation_vals = [safe_float(r.get("escalation_correct")) for r in rows]
    escalation_vals = [v for v in escalation_vals if v is not None]
    escalation_rate = sum(escalation_vals) / len(escalation_vals) if escalation_vals else None

    quality_scores = [safe_float(r.get("overall_quality_score")) for r in rows]
    quality_scores = [v for v in quality_scores if v is not None]
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else None

    def avg_col(col: str) -> Optional[float]:
        vals = [safe_float(r.get(col)) for r in rows]
        vals = [v for v in vals if v is not None]
        return sum(vals) / len(vals) if vals else None

    low_quality = [r for r in rows if safe_float(r.get("overall_quality_score"), 1.0) < 0.4]

    return {
        "total_questions": n,
        "source_match_rate": round(source_match_rate, 4) if source_match_rate is not None else None,
        "escalation_accuracy": round(escalation_rate, 4) if escalation_rate is not None else None,
        "avg_overall_quality": round(avg_quality, 4) if avg_quality is not None else None,
        "avg_answer_relevance": avg_col("answer_relevance_score"),
        "avg_groundedness": avg_col("groundedness_score"),
        "avg_completeness": avg_col("completeness_score"),
        "avg_unsupported_claim_risk": avg_col("unsupported_claim_risk_score"),
        "low_quality_count": len(low_quality),
        "low_quality_rows": low_quality,
    }


def get_low_quality_rows(rows: List[Dict], threshold: float = 0.4) -> List[Dict]:
    """Return rows where overall_quality_score < threshold."""
    return [r for r in rows if safe_float(r.get("overall_quality_score"), 1.0) < threshold]


def get_failed_source_match_rows(rows: List[Dict]) -> List[Dict]:
    """Return rows where source_match == 0."""
    return [r for r in rows if safe_float(r.get("source_match")) == 0.0]


def get_failed_escalation_rows(rows: List[Dict]) -> List[Dict]:
    """Return rows where escalation_correct == 0."""
    return [r for r in rows if safe_float(r.get("escalation_correct")) == 0.0]


def group_by_risk_category(rows: List[Dict]) -> Dict[str, Dict]:
    """
    Group rows by risk_category and compute avg quality + count per category.
    """
    groups = {}
    for r in rows:
        cat = r.get("risk_category", "Unknown").strip()
        if not cat:
            cat = "Unknown"
        if cat not in groups:
            groups[cat] = {"rows": [], "count": 0}
        groups[cat]["rows"].append(r)
        groups[cat]["count"] += 1

    result = {}
    for cat, data in groups.items():
        scores = [safe_float(r.get("overall_quality_score")) for r in data["rows"]]
        scores = [s for s in scores if s is not None]
        avg = sum(scores) / len(scores) if scores else None
        result[cat] = {
            "count": data["count"],
            "avg_overall_quality": round(avg, 4) if avg is not None else None,
        }
    return result


def group_by_difficulty(rows: List[Dict]) -> Dict[str, Dict]:
    """
    Group rows by difficulty_level and compute avg quality + count per level.
    """
    groups = {}
    for r in rows:
        d = r.get("difficulty_level", "Unknown").strip()
        if not d:
            d = "Unknown"
        if d not in groups:
            groups[d] = {"rows": [], "count": 0}
        groups[d]["rows"].append(r)
        groups[d]["count"] += 1

    result = {}
    for diff, data in groups.items():
        scores = [safe_float(r.get("overall_quality_score")) for r in data["rows"]]
        scores = [s for s in scores if s is not None]
        avg = sum(scores) / len(scores) if scores else None
        result[diff] = {
            "count": data["count"],
            "avg_overall_quality": round(avg, 4) if avg is not None else None,
        }
    return result
