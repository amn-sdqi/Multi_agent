"""Smart analysis tool for data operations."""

from langchain.tools import tool
from datetime import datetime
from core.executor import execute_code
from utils.formatters import format_result, classify_query_complexity
from utils.code_generators import generate_code, generate_summary

# Global variables for state management
from core import state

def set_global_data(df, schema_data):
    state.global_df = df
    state.schema = schema_data

def get_last_result():
    return state.last_analysis_result

@tool
def smart_analysis_tool(query: str) -> str:
    """
    Performs data analysis operations including basic display, statistics, 
    exploration, and complex analysis. Use for any dataset questions.
    """
    global last_analysis_result
    
    if state.global_df is None:
        return "No dataset loaded. Please load a dataset first."
    
    complexity = classify_query_complexity(query)
    
    try:
        code = generate_code(query, state.schema)
        raw_result = execute_code(code, state.global_df)
        formatted_result = format_result(raw_result)
        
        # Check for execution errors
        if "Error:" in str(raw_result):
            summary = f"Analysis failed: {raw_result}"
        else:
            if complexity == "simple":
                summary = f"{query}"
            else:
                summary = generate_summary(query, formatted_result, code)
        
        # Store result
        last_analysis_result = {
            'query': query,
            'summary': summary,
            'raw_result': formatted_result,
            'code': code,
            'complexity': complexity,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        
        # Return formatted response
        response = f"**Analysis Summary:**\n{summary}\n\n**Result:**\n{formatted_result}"
        if complexity == "complex":
            response += f"\n\n**Code Used:** {code}"
        
        return response
        
    except Exception as e:
        error_msg = f"Analysis error: {str(e)}"
        last_analysis_result = {
            'query': query,
            'summary': error_msg,
            'raw_result': error_msg,
            'code': 'N/A',
            'complexity': 'error',
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        return error_msg