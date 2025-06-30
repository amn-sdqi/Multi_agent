# """Suggestion tool for generating analysis recommendations."""

from langchain.tools import tool
from core.llm import llm_call

# Reference to schema
from core import state

@tool
def suggestion_tool(input_text: str) -> str:
    """Generate valid analysis questions based on dataset schema and types."""
    if not state.schema:
        return "No dataset loaded. Please load a dataset first to get suggestions."

    prompt = f"""
    You are a smart data analysis assistant.

    Based on the dataset schema below (which includes column names and types), generate exactly 5 or 6 specific and valid **natural language analysis questions** a user might ask.

    Only ask questions that are logically valid for the **column's data type**.

    Rules:
    - For **categorical columns**, you can ask about:
        • Most/least common category
        • Category-wise distribution
        • Count of unique categories
        • Relationships with other categorical or numerical columns
    - For **numerical columns**, you can ask about:
        • Average, min, max, sum, distribution
        • Correlation with other columns
        • Trends over time (if there's a date column)
    - For **date columns**, you can ask about:
        • Trends over time
        • Time-based grouping (daily, monthly, yearly)
    - DO NOT ask about impossible analysis (e.g., "sum of a category")

    Format:
    Return only the questions as a clean numbered list.
    Do NOT include explanations, markdown, or extra characters.

    Schema:
    {state.schema}

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
