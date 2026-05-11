# type: ignore

"""
Merlin UK Customer Opportunity Assistant
========================================
A lightweight Streamlit chatbot that lets business users ask natural-language
questions about the geographic customer segmentation dataset.

The assistant uses a two-step LLM pattern:
1. Generate pandas query code from the user's question + dataset documentation.
2. Execute the code and synthesize a concise, executive-friendly answer.

Dependencies (not in stdlib):
    pip install streamlit openai pandas

API key:
    Set OPENAI_API_KEY as an environment variable or in .streamlit/secrets.toml
"""

import os
import re
from pathlib import Path

import pandas as pd
import streamlit as st
from openai import OpenAI
from load_dotenv import load_dotenv

load_dotenv(override=True)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Merlin Opportunity Assistant",
    page_icon="🎢",
    layout="wide",
)

st.title("🎢 Merlin UK Customer Opportunity Assistant")
st.caption(
    "Ask natural-language questions about geographic customer segments, "
    "attraction opportunities, and media activation recommendations."
)

# ---------------------------------------------------------------------------
# Load data & documentation
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_resources():
    """Load the opportunity dataset and the dataset documentation."""
    csv_candidates = [
        "msoa_attraction_opportunities.csv",
        "data/msoa_attraction_opportunities.csv",
    ]
    csv_path = None
    for cand in csv_candidates:
        if Path(cand).exists():
            csv_path = cand
            break

    if csv_path is None:
        st.error(
            "Dataset 'msoa_attraction_opportunities.csv' not found. "
            "Please place it in the project root or in a 'data/' folder."
        )
        st.stop()

    df = pd.read_csv(csv_path)

    docs_path = "dataset_documentation.md"
    if not Path(docs_path).exists():
        st.error(f"Documentation file '{docs_path}' not found.")
        st.stop()

    with open(docs_path, "r", encoding="utf-8") as f:
        docs = f.read()

    return df, docs

with st.spinner("Loading dataset..."):
    df, DOCS = load_resources()

# ---------------------------------------------------------------------------
# Sidebar: setup & examples
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    # API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("OPENAI_API_KEY", None)
        except Exception:
            api_key = None

    if not api_key:
        st.warning(
            "No `OPENAI_API_KEY` detected.\n\n"
            "Set it as an environment variable or in `.streamlit/secrets.toml`:"
        )
        st.code("OPENAI_API_KEY = 'sk-...'", language="toml")
        st.stop()

    # Model selection
    model = st.selectbox(
        "OpenAI model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0,
        help="gpt-4o-mini is recommended: fast, cheap, and excellent at code generation.",
    )

    st.divider()
    st.header("💡 Example questions")
    example_questions = [
        "Which areas are highest opportunity for LEGOLAND?",
        "Where should Merlin target family annual passes?",
        "Which regions appear underpenetrated?",
        "What segment is Birmingham in?",
        "How far is Manchester from Alton Towers?",
        "What activation strategy fits struggling young families?",
    ]
    for q in example_questions:
        if st.button(q, use_container_width=True):
            st.session_state["example_query"] = q
            st.rerun()

    st.divider()
    st.caption(
        f"Dataset loaded: **{len(df):,}** rows × **{len(df.columns)}** columns."
    )

# ---------------------------------------------------------------------------
# OpenAI client
# ---------------------------------------------------------------------------
client = OpenAI(api_key=api_key)

# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------
CODE_SYSTEM_PROMPT = f"""You are an expert business-intelligence assistant for Merlin Entertainments UK.

You have access to a pandas DataFrame named `df` and the following documentation about its columns, segments, and business rules:

---
{DOCS}
---

INSTRUCTIONS:
1. If the user's question can be answered using the DataFrame, respond with **only** a Python code block.
   - The code must be valid pandas code.
   - The final answer must be assigned to a variable named `result` (e.g., `result = df.nlargest(5, ...)`).
   - Do NOT include explanations, markdown bullets, or anything outside the code block.
2. If the user's question does NOT require querying the dataset (e.g., "What does Cluster 1 mean?"), answer directly in natural language with no code block.
3. Always prefer concise, executive-friendly outputs. Filter to the top N rows rather than returning entire tables.
4. Use exact attraction names as they appear in the DataFrame (e.g., 'LEGOLAND® Windsor Resort').
"""

SYNTHESIS_SYSTEM_PROMPT = (
    "You are a helpful business-intelligence assistant. "
    "Convert the provided data result into a concise, executive-friendly natural language answer. "
    "Do not mention the code, DataFrame, or technical steps unless the user explicitly asked. "
    "When relevant, include actionable commercial recommendations."
)

# ---------------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render existing chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
default_query = st.session_state.pop("example_query", None)
user_input = st.chat_input("Ask a question about the data...", key="chat_input")
if default_query:
    user_input = default_query

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # -------------------------------------------------------------------
        # Step 1: ask the LLM to generate code or a direct answer
        # -------------------------------------------------------------------
        with st.spinner("Analysing question..."):
            code_gen_messages = [
                {"role": "system", "content": CODE_SYSTEM_PROMPT},
            ] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            response = client.chat.completions.create(
                model=model,
                messages=code_gen_messages,
                temperature=0.1,
            )
            raw_reply = response.choices[0].message.content.strip()

        # -------------------------------------------------------------------
        # Step 2: determine if we have code to run
        # -------------------------------------------------------------------
        code_match = re.search(r"```python\n(.*?)\n```", raw_reply, re.DOTALL)

        if code_match:
            python_code = code_match.group(1).strip()

            with st.expander("🔍 View generated query"):
                st.code(python_code, language="python")

            # Safe execution environment
            allowed_builtins = {
                "len": len,
                "range": range,
                "sorted": sorted,
                "list": list,
                "dict": dict,
                "str": str,
                "int": int,
                "float": float,
                "round": round,
                "sum": sum,
                "max": max,
                "min": min,
                "abs": abs,
                "zip": zip,
                "enumerate": enumerate,
            }
            exec_globals = {
                "__builtins__": allowed_builtins,
                "df": df,
                "pd": pd,
            }
            exec_locals = {}

            try:
                exec(python_code, exec_globals, exec_locals)
                result = exec_locals.get("result")

                if result is None:
                    raise ValueError(
                        "The generated code did not define a `result` variable."
                    )

                # Serialise result for the synthesis step
                if isinstance(result, pd.DataFrame):
                    result_text = result.head(20).to_string(index=False)
                elif isinstance(result, pd.Series):
                    result_text = result.head(20).to_string()
                else:
                    result_text = str(result)

            except Exception as e:
                error_msg = f"Error running generated code: {type(e).__name__}: {e}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
                st.stop()

            # ---------------------------------------------------------------
            # Step 3: synthesise natural-language answer from the result
            # ---------------------------------------------------------------
            with st.spinner("Synthesising answer..."):
                synthesis_prompt = (
                    f"User question: {user_input}\n\n"
                    f"Data result:\n{result_text}\n\n"
                    "Provide a concise, natural language answer. "
                    "Include any relevant commercial recommendations."
                )

                synthesis_response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYNTHESIS_SYSTEM_PROMPT},
                        {"role": "user", "content": synthesis_prompt},
                    ],
                    temperature=0.2,
                )
                final_answer = synthesis_response.choices[0].message.content.strip()

            st.markdown(final_answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": final_answer}
            )

        else:
            # Direct natural-language answer (no code required)
            st.markdown(raw_reply)
            st.session_state.messages.append(
                {"role": "assistant", "content": raw_reply}
            )
