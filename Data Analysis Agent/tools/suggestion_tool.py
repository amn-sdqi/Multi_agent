"""Suggestion tool for generating analysis recommendations."""

from langchain.tools import tool
from core.llm import llm_call

# Reference to schema
from core import state

@tool
def suggestion_tool(input_text: str) -> str:
    """Generate analysis suggestions based on dataset."""
    if not state.schema:
        return "No dataset loaded. Please load a dataset first to get suggestions."
    prompt = f"""
    You are a data analysis assistant.

    Based on the given dataset schema below, generate exactly 5 to 6 specific, insightful, and **concise natural language questions** that a user might ask for analysis.

    **Important instructions:**
    - ONLY return the questions.
    - DO NOT add any explanations or asterisks.
    - Format as a clean, numbered list.

    Schema: {state.schema}

    Format:
    1. Question one
    2. Question two
    ...
    """

    
    try:
        suggestions = llm_call(prompt)
        return suggestions
    except Exception as e:
        return f"Could not generate suggestions: {str(e)}"