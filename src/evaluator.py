"""
LLM-as-judge evaluator and rule-based metrics for the RAG system.

Supports two evaluator backends (set via EVALUATOR_PROVIDER):
  - gemini: uses google-genai SDK
  - groq: uses OpenAI-compatible API (for Mistral models like ministral-8b-2512)

Rule-based metrics (no LLM call needed):
  - source_match: did the expected document appear in retrieved sources?
  - escalation_correct: did the answer's escalation decision match expected?
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple

from src.config import (
    EVALUATOR_PROVIDER,
    EVALUATOR_MODEL_NAME,
    GEMINI_API_KEY,
    GROQ_API_KEY,
    GROQ_BASE_URL,
    MISTRAL_API_KEY,
    MISTRAL_BASE_URL,
    LLM_TEMPERATURE,
)

PLACEHOLDER_MARKERS = ["paste_your", "your_key", "your_api_key", "placeholder"]


def _is_placeholder_key(key: str) -> bool:
    lower = key.lower()
    return any(marker in lower for marker in PLACEHOLDER_MARKERS)


JUDGE_SYSTEM_PROMPT = """
You are a strict RAG evaluation judge. Your task is to score an AI assistant's
answer to a customer support question about SME policy documents.

You will receive:
- The user's question
- The expected answer summary (ground truth)
- The retrieved policy context (the documents the assistant had access to)
- The assistant's generated answer

Score the answer on these four dimensions, each from 1 (worst) to 5 (best):

1. answer_relevance_score
   - 5: Directly answers the question with no irrelevant content.
   - 3: Partially answers but includes some irrelevant detail.
   - 1: Does not answer the question at all.

2. groundedness_score
   - 5: Every claim is supported by the retrieved context. No hallucination.
   - 3: Most claims are supported but one or two lack clear evidence.
   - 1: Multiple claims are unsupported or directly contradict the context.

3. completeness_score
   - 5: Covers all key information from the expected answer summary.
   - 3: Covers the main point but misses important details.
   - 1: Misses almost all expected information.

4. unsupported_claim_risk_score
   - 5: No unsupported claims. Low risk. (Best)
   - 3: One or two minor unsupported claims but overall low risk.
   - 1: Major unsupported claims that could cause real harm. (Worst)

Return ONLY valid JSON with no markdown, no code fences, no extra text:
{
  "answer_relevance_score": <int 1-5>,
  "groundedness_score": <int 1-5>,
  "completeness_score": <int 1-5>,
  "unsupported_claim_risk_score": <int 1-5>,
  "evaluator_notes": "brief explanation of the scores"
}
"""


def build_evaluator_client():
    """
    Create and return an API client for the configured evaluator provider.
    Returns either a genai.Client (Gemini) or an openai.OpenAI client (Groq).
    """
    provider = EVALUATOR_PROVIDER.lower()

    if provider in ("gemini",):
        from google import genai
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set.\n"
                "Create a .env file with:\n"
                "  GEMINI_API_KEY=your_actual_key\n"
                "Get a free key at: https://aistudio.google.com/apikey"
            )
        if _is_placeholder_key(GEMINI_API_KEY):
            raise ValueError(
                "GEMINI_API_KEY is still set to the placeholder value.\n"
                "Open .env and replace PASTE_YOUR_GEMINI_API_KEY_HERE with your actual key."
            )
        return genai.Client(api_key=GEMINI_API_KEY)

    elif provider in ("groq",):
        from openai import OpenAI
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set.\n"
                "Create a .env file with:\n"
                "  GROQ_API_KEY=your_actual_key\n"
                "Get a free key at: https://console.groq.com"
            )
        if _is_placeholder_key(GROQ_API_KEY):
            raise ValueError(
                "GROQ_API_KEY is still set to the placeholder value.\n"
                "Open .env and replace PASTE_YOUR_GROQ_API_KEY_HERE with your actual key."
            )
        return OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

    elif provider in ("mistral",):
        from openai import OpenAI
        if not MISTRAL_API_KEY:
            raise ValueError(
                "MISTRAL_API_KEY is not set.\n"
                "Create a .env file with:\n"
                "  MISTRAL_API_KEY=your_actual_key\n"
                "Get a free key at: https://console.mistral.ai"
            )
        if _is_placeholder_key(MISTRAL_API_KEY):
            raise ValueError(
                "MISTRAL_API_KEY is still set to the placeholder value.\n"
                "Open .env and replace PASTE_YOUR_MISTRAL_API_KEY_HERE with your actual key."
            )
        return OpenAI(api_key=MISTRAL_API_KEY, base_url=MISTRAL_BASE_URL)

    else:
        raise ValueError(f"Unknown EVALUATOR_PROVIDER: {EVALUATOR_PROVIDER}. Use 'gemini' or 'groq'.")


def judge_answer(
    question: str,
    expected_answer: str,
    context_text: str,
    generated_answer: str,
) -> Dict:
    """
    Use the configured LLM-as-judge to score the generated answer.

    Returns a dict with score fields and evaluator_notes.
    On failure (JSON parse error, API error), returns a dict with
    scores set to None and evaluator_notes describing the error.
    """
    default_result = {
        "answer_relevance_score": None,
        "groundedness_score": None,
        "completeness_score": None,
        "unsupported_claim_risk_score": None,
        "evaluator_notes": "",
    }

    try:
        client = build_evaluator_client()
    except ValueError as e:
        default_result["evaluator_notes"] = f"Evaluator setup error: {e}"
        return default_result

    user_prompt = (
        f"## Question\n{question}\n\n"
        f"## Expected Answer Summary\n{expected_answer}\n\n"
        f"## Retrieved Context\n{context_text}\n\n"
        f"## Generated Answer\n{generated_answer}\n\n"
        f"Score the generated answer using the rubric above. Return JSON only."
    )

    provider = EVALUATOR_PROVIDER.lower()
    raw_text = ""

    try:
        if provider == "gemini":
            from google.genai import types as genai_types
            response = client.models.generate_content(
                model=EVALUATOR_MODEL_NAME,
                contents=user_prompt,
                config=genai_types.GenerateContentConfig(
                    system_instruction=JUDGE_SYSTEM_PROMPT,
                    temperature=0.0,
                    max_output_tokens=512,
                ),
            )
            raw_text = response.text.strip()
        elif provider in ("groq", "mistral", "openai"):
            response = client.chat.completions.create(
                model=EVALUATOR_MODEL_NAME,
                messages=[
                    {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.0,
                max_tokens=512,
            )
            raw_text = response.choices[0].message.content.strip()
    except Exception as e:
        default_result["evaluator_notes"] = f"Evaluator API error: {e}"
        return default_result

    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
        raw_text = re.sub(r"\s*```$", "", raw_text)

    try:
        scores = json.loads(raw_text)
    except json.JSONDecodeError:
        default_result["evaluator_notes"] = (
            f"Failed to parse judge JSON. Raw response: {raw_text[:500]}"
        )
        return default_result

    return {
        "answer_relevance_score": scores.get("answer_relevance_score"),
        "groundedness_score": scores.get("groundedness_score"),
        "completeness_score": scores.get("completeness_score"),
        "unsupported_claim_risk_score": scores.get("unsupported_claim_risk_score"),
        "evaluator_notes": scores.get("evaluator_notes", ""),
    }


def parse_escalation(answer: str) -> Optional[str]:
    """Extract 'Escalation needed: Yes/No' from the generated answer."""
    for line in answer.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("escalation needed:"):
            match = re.search(r"(Yes|No)", stripped, re.IGNORECASE)
            if match:
                return match.group(1).lower()
    return None


def compute_source_match(retrieved_sources: List[Dict], expected_document: str) -> int:
    """
    Rule-based: 1 if the expected document filename appears in retrieved sources.
    """
    expected_lower = expected_document.strip().lower()
    for src in retrieved_sources:
        src_file = src.get("source_file", "").lower()
        if expected_lower in src_file:
            return 1
    return 0


def compute_escalation_correct(answer: str, should_escalate: str) -> Tuple[int, Optional[str]]:
    """
    Rule-based: compare predicted escalation decision with expected.
    Returns (1 or 0, predicted_label).
    """
    predicted = parse_escalation(answer)
    if predicted is None:
        return 0, None

    expected = should_escalate.strip().lower()
    correct = 1 if predicted == expected else 0
    return correct, predicted


def compute_overall_quality(result_row: Dict) -> Optional[float]:
    """
    Compute a normalized 0-1 overall quality score from all metrics.

    Rule-based metrics (0 or 1) are used as-is.
    LLM-judge metrics (1-5) are normalized to 0-1 by (score - 1) / 4.

    Returns None if any required score is missing.
    """
    components = []

    sm = result_row.get("source_match")
    if sm is not None:
        components.append(float(sm))

    ec = result_row.get("escalation_correct")
    if ec is not None:
        components.append(float(ec))

    for key in ["answer_relevance_score", "groundedness_score", "completeness_score", "unsupported_claim_risk_score"]:
        val = result_row.get(key)
        if val is not None:
            normalized = (val - 1) / 4.0
            components.append(max(0.0, min(1.0, normalized)))

    if not components:
        return None

    return round(sum(components) / len(components), 4)
