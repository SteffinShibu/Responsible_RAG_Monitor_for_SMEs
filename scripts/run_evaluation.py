"""
Batch evaluation script for the RAG system.

Runs each question from sample_test_questions.csv through the RAG pipeline,
computes rule-based metrics, optionally runs LLM-as-judge evaluation,
and saves results incrementally to data/evaluation_results.csv.

Usage:
    python scripts/run_evaluation.py --limit 5 --sleep 10
    python scripts/run_evaluation.py --resume --limit 5 --sleep 10
    python scripts/run_evaluation.py --start 10 --limit 5 --sleep 10
    python scripts/run_evaluation.py --limit 5 --skip-llm-judge
    python scripts/run_evaluation.py --sleep 15
"""

import argparse
import csv
import sys
import time
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.rag_pipeline import answer_query
from src.evaluator import (
    compute_source_match,
    compute_escalation_correct,
    judge_answer,
    compute_overall_quality,
)
from src.config import (
    TEST_QUESTIONS_PATH,
    EVALUATION_RESULTS_PATH,
    EVALUATOR_PROVIDER,
    EVALUATOR_MODEL_NAME,
    GEMINI_API_KEY,
    GROQ_API_KEY,
    MISTRAL_API_KEY,
)
from src.generator import format_context
from src.utils import check_dependencies


FIELD_NAMES = [
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


def load_test_questions() -> list:
    """Load sample_test_questions.csv and return a list of dicts."""
    if not TEST_QUESTIONS_PATH.exists():
        print(f"Error: Test questions file not found at: {TEST_QUESTIONS_PATH}")
        sys.exit(1)

    with open(TEST_QUESTIONS_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        questions = []
        for row in reader:
            qid = row.get("question_id", "").strip()
            if not qid:
                continue
            questions.append(row)

    if not questions:
        print("Error: No valid questions found in sample_test_questions.csv")
        sys.exit(1)

    print(f"Loaded {len(questions)} test questions from {TEST_QUESTIONS_PATH}")
    return questions


def load_existing_results() -> dict:
    """Load any existing evaluation results, keyed by question_id."""
    existing = {}
    if not EVALUATION_RESULTS_PATH.exists():
        return existing

    with open(EVALUATION_RESULTS_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row.get("question_id", "").strip()
            if qid:
                existing[qid] = row
    print(f"Loaded {len(existing)} existing results from {EVALUATION_RESULTS_PATH}")
    return existing


def save_results(results: list, append: bool = True):
    """Save results to evaluation_results.csv. Creates file if not present."""
    mode = "a" if append else "w"
    file_exists = EVALUATION_RESULTS_PATH.exists()

    with open(EVALUATION_RESULTS_PATH, mode, encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        if not file_exists or not append:
            writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Saved {len(results)} rows to {EVALUATION_RESULTS_PATH}")


def print_summary(results: list, is_final: bool = True):
    """Print a terminal summary of evaluation results."""
    n = len(results)

    if n == 0:
        print("\nNo results to summarize.")
        return

    # Rule-based averages
    source_match_rate = sum(1 for r in results if r.get("source_match") == 1) / n * 100
    escalation_ok = sum(1 for r in results if r.get("escalation_correct") == 1) / n * 100

    # LLM-judge averages (skip None values)
    relevance_scores = [r["answer_relevance_score"] for r in results if r.get("answer_relevance_score") is not None]
    groundedness_scores = [r["groundedness_score"] for r in results if r.get("groundedness_score") is not None]
    completeness_scores = [r["completeness_score"] for r in results if r.get("completeness_score") is not None]
    risk_scores = [r["unsupported_claim_risk_score"] for r in results if r.get("unsupported_claim_risk_score") is not None]
    quality_scores = [r["overall_quality_score"] for r in results if r.get("overall_quality_score") is not None]

    avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else None
    avg_groundedness = sum(groundedness_scores) / len(groundedness_scores) if groundedness_scores else None
    avg_completeness = sum(completeness_scores) / len(completeness_scores) if completeness_scores else None
    avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else None
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else None

    # Count failed / low-quality cases
    low_quality = sum(1 for r in results if r.get("overall_quality_score") is not None and r["overall_quality_score"] < 0.4)
    failed_judge = sum(1 for r in results if r.get("evaluator_notes") and "Failed" in r["evaluator_notes"])

    print()
    print("=" * 60)
    print("  EVALUATION SUMMARY")
    print("=" * 60)
    print(f"  Questions evaluated in this run:  {n}")

    # Count total saved rows
    total_rows = 0
    if EVALUATION_RESULTS_PATH.exists():
        with open(EVALUATION_RESULTS_PATH, "r", encoding="utf-8") as f:
            total_rows = sum(1 for _ in csv.DictReader(f))
    print(f"  Total rows in results CSV:      {total_rows}")

    print()
    print("  ── Rule-based metrics ──")
    print(f"  Source match rate:              {source_match_rate:.1f}%")
    print(f"  Escalation accuracy:            {escalation_ok:.1f}%")

    print()
    print("  ── LLM-as-judge metrics (1-5 scale) ──")
    if avg_relevance is not None:
        print(f"  Average answer relevance:       {avg_relevance:.2f}")
    if avg_groundedness is not None:
        print(f"  Average groundedness:           {avg_groundedness:.2f}")
    if avg_completeness is not None:
        print(f"  Average completeness:           {avg_completeness:.2f}")
    if avg_risk is not None:
        print(f"  Average unsupported-claim risk: {avg_risk:.2f}  (5=low risk)")
    if avg_quality is not None:
        print(f"  Average overall quality (0-1):  {avg_quality:.4f}")

    if low_quality > 0:
        print(f"\n  ⚠️  Low-quality cases (score < 0.4): {low_quality}")
    if failed_judge > 0:
        print(f"  ⚠️  Failed LLM judge calls:          {failed_judge}")

    print(f"\n  Results CSV: {EVALUATION_RESULTS_PATH}")
    print("=" * 60)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Run batch evaluation of the RAG system."
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Maximum number of questions to evaluate in this run."
    )
    parser.add_argument(
        "--start", type=int, default=0,
        help="0-based index to start from in the questions list."
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Skip question_ids that already have results in evaluation_results.csv."
    )
    parser.add_argument(
        "--sleep", type=float, default=10.0,
        help="Seconds to wait between questions (default: 10)."
    )
    parser.add_argument(
        "--skip-llm-judge", action="store_true",
        help="Skip LLM-as-judge evaluation. Compute rule-based metrics only."
    )
    args = parser.parse_args()

    check_dependencies()

    # Warn about LLM judge if the appropriate API key is missing
    if not args.skip_llm_judge:
        provider = EVALUATOR_PROVIDER.lower()
        if provider == "gemini" and not GEMINI_API_KEY:
            print(
                "Warning: GEMINI_API_KEY is not set. LLM-as-judge evaluation will be "
                "skipped. Run with --skip-llm-judge to suppress this warning, or "
                "set GEMINI_API_KEY in .env."
            )
        elif provider == "groq" and not GROQ_API_KEY:
            print(
                "Warning: GROQ_API_KEY is not set. LLM-as-judge evaluation will be "
                "skipped. Run with --skip-llm-judge to suppress this warning, or "
                "set GROQ_API_KEY in .env."
            )
        elif provider == "mistral" and not MISTRAL_API_KEY:
            print(
                "Warning: MISTRAL_API_KEY is not set. LLM-as-judge evaluation will be "
                "skipped. Run with --skip-llm-judge to suppress this warning, or "
                "set MISTRAL_API_KEY in .env."
            )

    # Load questions
    all_questions = load_test_questions()

    # Load existing results for resume
    existing_results = {}
    if args.resume:
        existing_results = load_existing_results()
        print(f"Resume mode: {len(existing_results)} questions already evaluated.")

    # Determine the slice to process
    questions = all_questions[args.start:]
    if args.limit is not None:
        questions = questions[:args.limit]

    if not questions:
        print("No questions to evaluate.")
        return

    # Filter out already-evaluated questions if resuming
    if args.resume and existing_results:
        before = len(questions)
        questions = [q for q in questions if q["question_id"] not in existing_results]
        skipped = before - len(questions)
        if skipped > 0:
            print(f"Skipped {skipped} already-evaluated questions.")
        if not questions:
            print("All questions in this range have already been evaluated.")
            return

    print(f"\nEvaluating {len(questions)} questions...")
    if args.skip_llm_judge:
        print("LLM-as-judge: SKIPPED (--skip-llm-judge)")
    else:
        provider = EVALUATOR_PROVIDER.lower()
        model = EVALUATOR_MODEL_NAME
        print(f"LLM-as-judge: ENABLED ({provider} / {model})")

    new_results = []

    for idx, row in enumerate(questions):
        qid = row["question_id"]
        question = row["user_question"]
        print(f"\n[{idx + 1}/{len(questions)}] {qid}: {question[:60]}...")

        # Step 1: Run RAG pipeline
        try:
            rag_result = answer_query(question, top_k=5)
        except Exception as e:
            print(f"  ⚠️  RAG pipeline error: {e}")
            new_results.append({
                "question_id": qid,
                "user_question": question,
                "expected_answer_summary": row.get("expected_answer_summary", ""),
                "relevant_document": row.get("relevant_document", ""),
                "risk_category": row.get("risk_category", ""),
                "should_escalate": row.get("should_escalate", ""),
                "difficulty_level": row.get("difficulty_level", ""),
                "generated_answer": f"ERROR: {e}",
                "retrieved_sources": "",
                "source_match": 0,
                "predicted_escalation": "",
                "escalation_correct": 0,
                "answer_relevance_score": None,
                "groundedness_score": None,
                "completeness_score": None,
                "unsupported_claim_risk_score": None,
                "overall_quality_score": None,
                "evaluator_notes": f"RAG pipeline error: {e}",
            })
            save_results(new_results[-1:])  # save single row
            time.sleep(args.sleep)
            continue

        answer = rag_result["answer"]
        sources = rag_result["sources"]

        # Format sources for CSV storage
        source_summary = "; ".join(
            f"{s['source_file']} (score={s['similarity_score']})"
            for s in sources
        ) if sources else ""

        # Step 2: Rule-based metrics
        expected_doc = row.get("relevant_document", "")
        source_match = compute_source_match(sources, expected_doc)
        escalation_correct_val, predicted_esc = compute_escalation_correct(
            answer, row.get("should_escalate", "")
        )

        result_row = {
            "question_id": qid,
            "user_question": question,
            "expected_answer_summary": row.get("expected_answer_summary", ""),
            "relevant_document": expected_doc,
            "risk_category": row.get("risk_category", ""),
            "should_escalate": row.get("should_escalate", ""),
            "difficulty_level": row.get("difficulty_level", ""),
            "generated_answer": answer,
            "retrieved_sources": source_summary,
            "source_match": source_match,
            "predicted_escalation": predicted_esc if predicted_esc else "",
            "escalation_correct": escalation_correct_val,
            "answer_relevance_score": None,
            "groundedness_score": None,
            "completeness_score": None,
            "unsupported_claim_risk_score": None,
            "overall_quality_score": None,
            "evaluator_notes": "",
        }

        # Step 3: LLM-as-judge (optional)
        if not args.skip_llm_judge:
            provider = EVALUATOR_PROVIDER.lower()
            api_key_ok = (provider == "gemini" and bool(GEMINI_API_KEY)) or \
                         (provider == "groq" and bool(GROQ_API_KEY)) or \
                         (provider == "mistral" and bool(MISTRAL_API_KEY))
            if api_key_ok:
                print(f"  Running LLM-as-judge ({provider})...")
            try:
                # Build context text from retrieved sources
                context_text = format_context(sources) if sources else ""
                judge_scores = judge_answer(
                    question=question,
                    expected_answer=row.get("expected_answer_summary", ""),
                    context_text=context_text,
                    generated_answer=answer,
                )
                result_row["answer_relevance_score"] = judge_scores.get("answer_relevance_score")
                result_row["groundedness_score"] = judge_scores.get("groundedness_score")
                result_row["completeness_score"] = judge_scores.get("completeness_score")
                result_row["unsupported_claim_risk_score"] = judge_scores.get("unsupported_claim_risk_score")
                result_row["evaluator_notes"] = judge_scores.get("evaluator_notes", "")
            except Exception as e:
                result_row["evaluator_notes"] = f"LLM judge error: {e}"

        # Step 4: Compute overall quality
        result_row["overall_quality_score"] = compute_overall_quality(result_row)

        new_results.append(result_row)

        # Save incrementally (append single row)
        save_results([result_row])

        print(f"  ✅ Done. source_match={source_match}, escalation_ok={escalation_correct_val}")

        # Sleep between questions (not after the last one)
        if idx < len(questions) - 1 and args.sleep > 0:
            print(f"  Sleeping {args.sleep}s...")
            time.sleep(args.sleep)

    # Print summary
    print_summary(new_results)


if __name__ == "__main__":
    main()
