from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st

from src.faq_loader import load_faq_data, validate_faq_data
from src.generator import generate_support_answer
from src.lead_capture import save_lead
from src.retriever import FAQRetriever


DEFAULT_FAQ_PATH = Path("business_data/faq.csv")
LEADS_PATH = Path("business_data/leads.csv")

st.set_page_config(
    page_title="AI Customer Support Chatbot",
    page_icon="💬",
    layout="wide",
)

st.title("AI Customer Support Chatbot")
st.write(
    "Ask questions about a business using a simple FAQ knowledge base. "
    "The chatbot retrieves the most relevant answer and avoids guessing when the FAQ does not contain enough information."
)

with st.sidebar:
    st.header("Settings")

    min_score = st.slider(
        "Minimum match score",
        min_value=0.05,
        max_value=0.80,
        value=0.18,
        step=0.05,
        help="Higher values make the chatbot more careful. Lower values allow more flexible matching.",
    )

    top_k = st.slider(
        "Number of retrieved FAQ entries",
        min_value=1,
        max_value=5,
        value=3,
    )

    use_openai = st.checkbox(
        "Use OpenAI for answer rewriting",
        value=False,
        help="Requires OPENAI_API_KEY to be set in your environment.",
    )

    if use_openai and not os.getenv("OPENAI_API_KEY"):
        st.warning("OPENAI_API_KEY is not set. The app will use the retrieved FAQ answer directly.")

    st.divider()
    st.caption("Default demo: BrightCare Dental Clinic FAQ")

uploaded_faq = st.file_uploader(
    "Optional: upload your own FAQ CSV file",
    type=["csv"],
    help="CSV must include at least two columns: question and answer.",
)

try:
    if uploaded_faq is not None:
        faq_df = pd.read_csv(uploaded_faq)
    else:
        faq_df = load_faq_data(DEFAULT_FAQ_PATH)

    validate_faq_data(faq_df)

except Exception as exc:
    st.error(f"Could not load FAQ data: {exc}")
    st.stop()

retriever = FAQRetriever(faq_df)

left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_question = st.chat_input("Ask a customer support question...")

    if user_question:
        st.session_state.messages.append({"role": "user", "content": user_question})

        retrieved_items = retriever.search(
            query=user_question,
            top_k=top_k,
        )

        answer = generate_support_answer(
            question=user_question,
            retrieved_items=retrieved_items,
            min_score=min_score,
            use_openai=use_openai,
        )

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

with right_col:
    st.subheader("Knowledge Base")
    st.write(f"Loaded FAQ entries: **{len(faq_df)}**")

    with st.expander("View FAQ data"):
        st.dataframe(faq_df, use_container_width=True)

    st.subheader("Lead Request")

    with st.form("lead_form", clear_on_submit=True):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message or request")
        submitted = st.form_submit_button("Save lead")

        if submitted:
            if not name or not email or not message:
                st.warning("Please fill in name, email, and message.")
            else:
                save_lead(
                    leads_path=LEADS_PATH,
                    name=name,
                    email=email,
                    message=message,
                )
                st.success("Lead saved locally.")

    st.caption("Lead data is saved only in a local CSV file for demo purposes.")

st.divider()

with st.expander("Retrieved FAQ entries for the latest question"):
    if st.session_state.messages:
        last_user_questions = [
            message["content"]
            for message in st.session_state.messages
            if message["role"] == "user"
        ]

        if last_user_questions:
            latest_question = last_user_questions[-1]
            latest_retrieved = retriever.search(latest_question, top_k=top_k)

            for item in latest_retrieved:
                st.markdown(f"**Score:** {item.score:.3f}")
                st.markdown(f"**Question:** {item.question}")
                st.markdown(f"**Answer:** {item.answer}")
                st.divider()
    else:
        st.write("Ask a question to see retrieved FAQ entries.")

st.caption("Portfolio project: Python, Streamlit, scikit-learn, FAQ retrieval, optional OpenAI API.")
