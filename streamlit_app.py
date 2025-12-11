import os
import sys
import streamlit as st
import pandas as pd

# -------------------------------------------------
# Make src/ importable (project root is parent of this file)
# -------------------------------------------------
THIS_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(THIS_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.retrieval import TfidfRetriever
from src.qa import call_llm_ollama

# -------------------------------------------------
# 🔹 IMPORTANT: first Streamlit command
# -------------------------------------------------
st.set_page_config(
    page_title="Mastercard Intelligence Agent",
    page_icon="💳",
    layout="wide",
)

# -------------------------------------------------
# Cached loader so we don't rebuild TF–IDF on every run
# -------------------------------------------------
@st.cache_resource
def load_retriever():
    return TfidfRetriever("chunks.csv")


retriever = load_retriever()

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------
st.title("💳 Mastercard Intelligence Agent")
st.write(
    "Ask questions about Mastercard based on its 10-K, Sustainability Bond Report, "
    "and related documents. Answers are grounded in those documents only."
)

st.sidebar.header("Settings")

top_k = st.sidebar.slider("Number of chunks to retrieve", min_value=3, max_value=10, value=5)

example_questions = [
    "What does Mastercard do as a business?",
    "What are Mastercard's main strategic priorities?",
    "What risks does Mastercard face?",
    "What are Mastercard's sustainability or ESG goals?",
    "Summarize Mastercard's financial performance."
]

example_choice = st.sidebar.selectbox("Example questions", ["(none)"] + example_questions)

st.sidebar.markdown("---")
st.sidebar.write("⚠️ Make sure Ollama is running (e.g., `ollama list` works in a terminal).")

default_q = "" if example_choice == "(none)" else example_choice
question = st.text_input("Enter your question about Mastercard:", value=default_q)

ask_btn = st.button("Ask")

if ask_btn and question.strip():
    with st.spinner("Retrieving relevant document chunks..."):
        chunks_df = retriever.retrieve(question, k=top_k)

    st.subheader("Answer")

    try:
        with st.spinner("Thinking with local LLM via Ollama..."):
            answer = call_llm_ollama(question, chunks_df, model="llama3")
        st.write(answer)
    except Exception as e:
        st.error(
            "Error calling Ollama. Make sure Ollama is installed, running, and the model "
            "`llama3` is pulled. Error details:"
        )
        st.code(str(e))

    with st.expander("Show retrieved chunks"):
        for _, row in chunks_df.iterrows():
            st.markdown(
                f"**{row['chunk_id']}**  \n"
                f"*Source*: {row['source_file']}  \n"
                f"*Pages*: {row['page_start']}–{row['page_end']}  \n"
                f"*Score*: {row['score']:.4f}"
            )
            st.write(row["chunk_text"][:800] + "...")
            st.markdown("---")

elif ask_btn and not question.strip():
    st.warning("Please enter a question before clicking 'Ask'.")


