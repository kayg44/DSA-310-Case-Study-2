# src/qa.py

import textwrap
import pandas as pd
import re


def build_context_from_chunks(chunks_df, max_chars=9000):
    """
    Convert retrieved chunks into a formatted block of text
    that will be injected into the LLM prompt.
    """
    lines = []
    total_len = 0

    for _, row in chunks_df.iterrows():
        header = (
            f"[{row['chunk_id']}] "
            f"(source: {row['source_file']}, "
            f"pages {row['page_start']}-{row['page_end']})"
        )
        body = str(row["chunk_text"])

        block = header + "\n" + body + "\n\n"

        # Prevent prompt exceeding model token limits
        if total_len + len(block) > max_chars:
            break

        lines.append(block)
        total_len += len(block)

    return "".join(lines)


def build_qa_prompt(question, chunks_df):
    """
    Create the prompt for the LLM,
    including rules, context, and the question.
    """

    context = build_context_from_chunks(chunks_df)

    prompt = f"""
You are a careful financial and ESG analyst for Mastercard.
You must answer questions using ONLY the information from the provided document chunks.

QUESTION:
{question}

CONTEXT (document chunks):
---------------------------
{context}
---------------------------

Answer the QUESTION using ONLY the CONTEXT above. Follow these rules strictly:

1. Do NOT use any outside knowledge. If the answer is not clearly supported by the context, say:
   "I cannot find an answer in the provided documents."

2. Every factual statement must include a citation with the chunk id in square brackets.
   Example: Mastercard's revenue increased in 2024. [chunk_12]

3. If multiple chunks support the answer, cite all of them, e.g. [chunk_3, chunk_7].

4. Be concise, structured, and factual.

5. At the end of your answer, include:
   "Sources: [chunk_x, chunk_y, ...]"
""".strip()

    return prompt


def call_llm_ollama(question, chunks_df, model="llama3"):
    """
    Sends the prompt to a local Ollama model
    and returns the generated answer.
    """
    import ollama  # local model client

    prompt = build_qa_prompt(question, chunks_df)

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # The text output from Ollama is inside:
    return response["message"]["content"]
