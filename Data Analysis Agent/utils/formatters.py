"""Result formatting utilities."""

import pandas as pd
from typing import Any
from config.settings import MAX_DISPLAY_ROWS, MAX_OUTPUT_LENGTH

def format_result(result: Any) -> str:
    """Format result with automatic truncation."""
    if isinstance(result, pd.DataFrame):
        if len(result) > MAX_DISPLAY_ROWS:
            formatted = result.head(MAX_DISPLAY_ROWS).to_string(index=True)
            return f"DataFrame with {len(result)} rows (showing first {MAX_DISPLAY_ROWS}):\n{formatted}\n... ({len(result) - MAX_DISPLAY_ROWS} more rows)"
        return result.to_string(index=True)
    elif isinstance(result, pd.Series):
        if len(result) > MAX_DISPLAY_ROWS:
            formatted = result.head(MAX_DISPLAY_ROWS).to_string()
            return f"Series with {len(result)} values (showing first {MAX_DISPLAY_ROWS}):\n{formatted}\n... ({len(result) - MAX_DISPLAY_ROWS} more values)"
        return result.to_string()
    
    result_str = str(result)
    if len(result_str) > MAX_OUTPUT_LENGTH:
        return result_str[:MAX_OUTPUT_LENGTH] + f"... (truncated, {len(result_str) - MAX_OUTPUT_LENGTH} more characters)"
    return result_str

def classify_query_complexity(query: str) -> str:
    """Classify query complexity using simple keywords."""
    simple_keywords = ['head', 'tail', 'info', 'describe', 'shape', 'show', 'display', 'first', 'last']
    return "simple" if any(keyword in query.lower() for keyword in simple_keywords) else "complex"