import pandas as pd

from src.retriever import FAQRetriever


def test_retriever_finds_relevant_answer():
    df = pd.DataFrame(
        {
            "category": ["Hours", "Payments"],
            "question": ["What are your opening hours?", "What payment methods do you accept?"],
            "answer": ["We are open Monday to Friday.", "We accept card and cash."],
        }
    )

    retriever = FAQRetriever(df)
    results = retriever.search("When are you open?", top_k=1)

    assert len(results) == 1
    assert "open" in results[0].answer.lower()


def test_retriever_returns_empty_for_blank_query():
    df = pd.DataFrame(
        {
            "question": ["What services do you provide?"],
            "answer": ["We provide dental services."],
        }
    )

    retriever = FAQRetriever(df)
    results = retriever.search("   ", top_k=1)

    assert results == []
