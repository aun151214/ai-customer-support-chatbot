from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class RetrievedFAQ:
    question: str
    answer: str
    score: float
    category: str = ""


class FAQRetriever:
    def __init__(self, faq_df: pd.DataFrame):
        self.faq_df = faq_df.copy()

        if "category" not in self.faq_df.columns:
            self.faq_df["category"] = ""

        self.documents = (
            self.faq_df["category"].fillna("").astype(str)
            + " "
            + self.faq_df["question"].fillna("").astype(str)
            + " "
            + self.faq_df["answer"].fillna("").astype(str)
        ).tolist()

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.documents)

    def search(self, query: str, top_k: int = 3) -> list[RetrievedFAQ]:
        if not query.strip():
            return []

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).flatten()

        ranked_indices = scores.argsort()[::-1][:top_k]

        results: list[RetrievedFAQ] = []

        for index in ranked_indices:
            row = self.faq_df.iloc[index]
            results.append(
                RetrievedFAQ(
                    question=str(row["question"]),
                    answer=str(row["answer"]),
                    category=str(row.get("category", "")),
                    score=float(scores[index]),
                )
            )

        return results
