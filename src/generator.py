import re
from typing import List, Dict

from openai import OpenAI

from src.config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL_NAME, LLM_TEMPERATURE

# File extensions the model cannot handle — detect them in user queries
IMAGE_FILE_PATTERN = re.compile(
    r'(?:^|\s)(?:[^\s]+)?\.(?:png|jpg|jpeg|gif|bmp|webp|svg|ico|tiff?)(?:\s|$|\.)',
    re.IGNORECASE,
)
OTHER_FILE_PATTERN = re.compile(
    r'(?:^|\s)(?:[^\s]+)?\.(?:pdf|docx?|xlsx?|pptx?|zip|tar|gz|mp[34]|avi|mov)(?:\s|$|\.)',
    re.IGNORECASE,
)


SYSTEM_PROMPT = """
You are the BrightPath Office Supplies AI Assistant. Your job is to answer customer support questions using only the policy document excerpts provided below.

## Core Rules

1. Answer only using the retrieved policy context. Do not use any external knowledge or make up information.
2. If the context does not contain enough information to answer the question, state: "The policy documents do not provide enough information to answer this question."
3. Do not invent policies, refund approvals, legal claims, or operational details.
4. Do not promise refunds, replacements, compensation, or approvals unless the context clearly permits it.
5. Use clear, simple language suitable for an SME employee or customer.

## Escalation Rules

You must recommend human escalation when any of the following conditions are met:

- The query involves a transaction value over €500.00.
- The query involves privacy-sensitive data (BSN, GDPR, data deletion, credit card info).
- The query involves a legal threat, lawsuit, or regulatory complaint.
- The query involves an AI-related complaint or allegation of AI harm.
- The query involves medical or health-related claims or warranties.
- The query involves creating custom discounts, promotions, or pricing.
- The query involves a scenario that does not clearly fit any single policy (ambiguous or contradictory).
- The retrieved context contains a clear instruction to escalate (e.g., "route to human agent", "dual sign-off required").

## Output Format

At the end of your answer, include exactly these two lines:

Escalation needed: Yes/No
Reason: A brief one-sentence explanation of why escalation is or is not needed.

## Tone

Be professional, clear, and helpful. Use plain English. Do not be overly technical or legalistic. If you cannot answer, be honest about it and suggest escalation.
""".strip()


PLACEHOLDER_MARKERS = ["paste_your", "your_key", "your_api_key", "placeholder"]


def _is_placeholder_key(key: str) -> bool:
    """Check whether the API key value looks like an unedited placeholder."""
    lower = key.lower()
    return any(marker in lower for marker in PLACEHOLDER_MARKERS)


def _check_for_file_references(query: str) -> str:
    """Check if the query references an image or other file the model cannot process.

    Returns an empty string if the query is safe, or an error message if it looks
    like a file reference.
    """
    if IMAGE_FILE_PATTERN.search(query):
        return (
            "This assistant only supports text questions. "
            "Please ask your question without referencing image files "
            "(PNG, JPG, GIF, etc.)."
        )
    if OTHER_FILE_PATTERN.search(query):
        return (
            "This assistant only supports text questions. "
            "Please ask your question without referencing document or media files."
        )
    return ""


def build_groq_client() -> OpenAI:
    """
    Create and return an OpenAI-compatible client pointed at Groq.

    Raises:
        ValueError: if GROQ_API_KEY is not set or is still a placeholder.
    """
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not set.\n"
            "Create a .env file in the project root with:\n"
            "  GROQ_API_KEY=your_actual_key\n"
            "Get a free key at: https://console.groq.com"
        )
    if _is_placeholder_key(GROQ_API_KEY):
        raise ValueError(
            "GROQ_API_KEY is still set to the placeholder value.\n"
            "Open the .env file and replace:\n"
            "  GROQ_API_KEY=PASTE_YOUR_GROQ_API_KEY_HERE\n"
            "with your actual Groq API key.\n"
            "Get a free key at: https://console.groq.com"
        )
    return OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)


def format_context(chunks: List[Dict]) -> str:
    """
    Format retrieved chunks into a block of context text for the LLM.

    Each chunk includes its source filename, section heading, and text.
    """
    parts = []
    for i, chunk in enumerate(chunks, 1):
        section = f" (Section: {chunk['section_heading']})" if chunk["section_heading"] else ""
        parts.append(
            f"[Document {i}]: {chunk['source_file']}{section}\n"
            f"{chunk['text']}"
        )
    return "\n\n".join(parts)


def generate_answer(query: str, chunks: List[Dict]) -> str:
    """
    Generate a grounded answer using Groq (via OpenAI-compatible API),
    given a query and retrieved chunks.

    Args:
        query: the user's question.
        chunks: list of retrieved chunk dicts from the retriever.

    Returns:
        The generated answer text.

    Raises:
        ValueError: if API key is missing or invalid, or if the query
                    references a file the model cannot process.
        RuntimeError: if the Groq API call fails due to an unsupported
                      input type (e.g., image reference).
        Exception: if the Groq API call fails for other reasons.
    """
    # Input validation: reject file references early
    file_error = _check_for_file_references(query)
    if file_error:
        raise ValueError(file_error)

    client = build_groq_client()

    context = format_context(chunks)

    user_prompt = (
        f"Question: {query}\n\n"
        f"Retrieved policy context:\n{context}\n\n"
        f"Please answer the question using only the context above."
    )

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=LLM_TEMPERATURE,
            max_tokens=1024,
        )
    except Exception as e:
        error_str = str(e).lower()
        if "image" in error_str or "does not support" in error_str:
            raise RuntimeError(
                "The AI model does not support image or file input. "
                "Please ask a text-only question about BrightPath policies."
            ) from e
        raise

    return response.choices[0].message.content
