"""
Statistical Process Control (SPC) monitoring for evaluation results.

Implements Shewhart control chart with 3-sigma limits and selected Nelson rules.

Nelson rules implemented:
  - Rule 1: One point beyond 3 standard deviations from the mean
  - Rule 2: Nine points in a row on the same side of the mean
  - Rule 3: Six points in a row steadily increasing or decreasing
"""

from typing import Dict, List, Optional

from src.evaluation_analysis import safe_float


def compute_control_limits(scores: List[float]) -> Dict[str, float]:
    """
    Compute mean, standard deviation, UCL, and LCL for a list of scores.
    Clips LCL at 0 and UCL at 1 since scores are in [0, 1].
    """
    n = len(scores)
    if n < 2:
        return {
            "mean": scores[0] if n == 1 else 0,
            "std": 0,
            "ucl": 1,
            "lcl": 0,
            "n": n,
        }

    mean_val = sum(scores) / n
    variance = sum((s - mean_val) ** 2 for s in scores) / (n - 1)
    std_val = variance ** 0.5

    ucl = min(1.0, mean_val + 3 * std_val)
    lcl = max(0.0, mean_val - 3 * std_val)

    return {
        "mean": round(mean_val, 4),
        "std": round(std_val, 4),
        "ucl": round(ucl, 4),
        "lcl": round(lcl, 4),
        "n": n,
    }


def check_nelson_rule_1(score: float, mean_val: float, std_val: float) -> bool:
    """Rule 1: One point beyond 3 sigma from the mean."""
    if std_val == 0:
        return False
    return abs(score - mean_val) > 3 * std_val


def check_nelson_rule_2(scores: List[float], mean_val: float) -> bool:
    """Rule 2: Nine consecutive points on the same side of the mean."""
    if len(scores) < 9:
        return False
    for i in range(len(scores) - 8):
        segment = scores[i:i + 9]
        above = all(s >= mean_val for s in segment)
        below = all(s <= mean_val for s in segment)
        if above or below:
            return True
    return False


def check_nelson_rule_3(scores: List[float], lookback: int = 6) -> bool:
    """Rule 3: Six consecutive points steadily increasing or decreasing."""
    if len(scores) < lookback:
        return False
    for i in range(len(scores) - lookback + 1):
        segment = scores[i:i + lookback]
        increasing = all(segment[j] <= segment[j + 1] for j in range(lookback - 1))
        decreasing = all(segment[j] >= segment[j + 1] for j in range(lookback - 1))
        if increasing or decreasing:
            return True
    return False


def get_spc_flags(rows: List[Dict]) -> List[Dict]:
    """
    Compute SPC flags for each evaluation row.

    Returns a list of dicts with keys:
      index, question_id, overall_quality_score,
      rule_1_flag, rule_2_flag, rule_3_flag, combined_spc_flag
    """
    scores = []
    for r in rows:
        s = safe_float(r.get("overall_quality_score"))
        scores.append(s if s is not None else 0.0)

    if not scores:
        return []

    limits = compute_control_limits(scores)
    mean_val = limits["mean"]
    std_val = limits["std"]

    flags = []
    for i, row in enumerate(rows):
        score = scores[i]
        past_scores = scores[:i + 1]

        r1 = check_nelson_rule_1(score, mean_val, std_val)
        r2 = check_nelson_rule_2(past_scores, mean_val)
        r3 = check_nelson_rule_3(past_scores)

        flags.append({
            "index": i,
            "question_id": row.get("question_id", ""),
            "user_question": row.get("user_question", ""),
            "overall_quality_score": score,
            "rule_1_flag": r1,
            "rule_2_flag": r2,
            "rule_3_flag": r3,
            "combined_spc_flag": r1 or r2 or r3,
        })

    return flags
