"""
Lightweight productivity analysis module.

Reads synthetic productivity data and computes comparison statistics
between manual-only and AI-assisted support workflows.

This module uses synthetic data to demonstrate how an SME productivity
evaluation could be structured in a field intervention. In a real
deployment, this could be extended to panel or firm-level analysis
using difference-in-differences, fixed effects models, or count-data
approaches depending on the outcome variable.
"""

import csv
from pathlib import Path
from typing import Dict, List, Optional

PRODUCTIVITY_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "synthetic_productivity_data.csv"


def load_productivity_data(path: Optional[Path] = None) -> List[Dict]:
    p = path or PRODUCTIVITY_DATA_PATH
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_summary(rows: List[Dict]) -> Dict:
    if not rows:
        return {}

    manual_times = [float(r["manual_resolution_time_min"]) for r in rows]
    ai_times = [float(r["ai_assisted_resolution_time_min"]) for r in rows]
    manual_errors = sum(1 for r in rows if int(r["manual_error_flag"]) == 1)
    ai_errors = sum(1 for r in rows if int(r["ai_assisted_error_flag"]) == 1)
    escalations = sum(1 for r in rows if r["escalation_needed"].lower() == "yes")
    review_times = [float(r["human_review_time_min"]) for r in rows if float(r["human_review_time_min"]) > 0]
    final_times = [float(r["final_resolution_time_min"]) for r in rows]

    avg_manual = sum(manual_times) / len(manual_times) if manual_times else 0
    avg_ai = sum(ai_times) / len(ai_times) if ai_times else 0
    avg_final = sum(final_times) / len(final_times) if final_times else 0
    avg_review = sum(review_times) / len(review_times) if review_times else 0

    time_savings_pct = ((avg_manual - avg_ai) / avg_manual * 100) if avg_manual > 0 else 0

    return {
        "total_scenarios": len(rows),
        "avg_manual_time_min": round(avg_manual, 1),
        "avg_ai_assisted_time_min": round(avg_ai, 1),
        "avg_final_resolution_time_min": round(avg_final, 1),
        "avg_human_review_time_min": round(avg_review, 1),
        "time_savings_pct": round(time_savings_pct, 1),
        "manual_errors": manual_errors,
        "ai_assisted_errors": ai_errors,
        "error_reduction_pct": round((manual_errors - ai_errors) / manual_errors * 100, 1) if manual_errors > 0 else 0,
        "escalations": escalations,
    }


if __name__ == "__main__":
    data = load_productivity_data()
    if not data:
        print("No productivity data found.")
    else:
        s = compute_summary(data)
        print("=== Productivity Summary ===")
        print(f"Scenarios: {s['total_scenarios']}")
        print(f"Avg manual time: {s['avg_manual_time_min']} min")
        print(f"Avg AI-assisted time: {s['avg_ai_assisted_time_min']} min")
        print(f"Time savings: {s['time_savings_pct']}%")
        print(f"Manual errors: {s['manual_errors']}")
        print(f"AI-assisted errors: {s['ai_assisted_errors']}")
        print(f"Error reduction: {s['error_reduction_pct']}%")
        print(f"Escalations: {s['escalations']}")
        print(f"Avg final resolution: {s['avg_final_resolution_time_min']} min")
