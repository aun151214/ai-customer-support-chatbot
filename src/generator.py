from __future__ import annotations

import os
import re
from typing import Sequence

from .retriever import RetrievedFAQ


COMMON_WORDS = {
    "what", "who", "where", "when", "why", "how",
    "is", "are", "was", "were", "the", "a", "an",
    "of", "to", "in", "on", "for", "and", "or",
    "do", "does", "did", "can", "could", "would",
    "your", "you", "clinic", "business", "company",
    "provide", "available", "information",
}


def extract_keywords(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())
    return {word for word in words if word not in COMMON_WORDS}


def has_answer_support(question: str, retrieved_items: Sequence[RetrievedFAQ]) -> bool:
    if not retrieved_items:
        return False

    question_keywords = extract_keywords(question)

    if not question_keywords:
        return True

    context = " ".join(
        f"{item.category} {item.question} {item.answer}".lower()
        for item in retrieved_items
    )

    matched_keywords = {word for word in question_keywords if word in context}

    return len(matched_keywords) > 0


def build_context(items: Sequence[RetrievedFAQ]) -> str:
    context_parts = []

    for index, item in enumerate(items, start=1):
        context_parts.append(
            f"FAQ {index}\n"
            f"Category: {item.category}\n"
            f"Question: {item.question}\n"
            f"Answer: {item.answer}\n"
            f"Score: {item.score:.3f}"
        )

    return "\n\n".join(context_parts)


def generate_support_answer(
    question: str,
    retrieved_items: Sequence[RetrievedFAQ],
    min_score: float,
    use_openai: bool = False,
) -> str:
    if not retrieved_items:
        return (
            "I could not find a relevant answer in the FAQ. "
            "Please contact the support team or leave your details in the lead request form."
        )

    best_item = retrieved_items[0]

    if best_item.score < min_score or not has_answer_support(question, retrieved_items):
        return (
            "I could not find enough information in the FAQ to answer this confidently. "
            "Please contact the support team or leave your details in the lead request form."
        )

    if not use_openai or not os.getenv("OPENAI_API_KEY"):
        return best_item.answer

    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        context = build_context(retrieved_items)

        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            instructions=(
                "You are a helpful customer support assistant. "
                "Answer only using the provided FAQ context. "
                "If the FAQ does not contain the answer, say that the information is not available. "
                "Keep the answer clear, polite, and concise."
            ),
            input=f"FAQ context:\n{context}\n\nCustomer question: {question}",
        )

        return response.output_text

    except Exception as exc:
        return (
            best_item.answer
            + f"\n\nNote: OpenAI answer rewriting was not available. Reason: {exc}"
        )