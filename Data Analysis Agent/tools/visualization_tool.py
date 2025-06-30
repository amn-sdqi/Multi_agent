"""Visualization tool for creating charts and plots."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from langchain.tools import tool
from datetime import datetime
from core.llm import llm_call
from utils.code_generators import generate_viz_code
from utils.file_handlers import generate_image_path, save_plot, open_image

# Reference to global data 
from core import state


def execute_viz(code: str, df: pd.DataFrame) -> str:
    """Execute visualization code."""
    image_path = generate_image_path()
    try:
        context = {'df': df.copy(), 'plt': plt, 'sns': sns, 'np': np}
        exec(code, context)
        save_plot(image_path)
        return image_path
    except Exception as e:
        plt.close()
        return f"Visualization failed: {str(e)}"

@tool
def visualization_tool(query: str) -> str:
    """Create data visualizations with AI-generated code."""
    global last_analysis_result
    
    if state.global_df is None:
        return "No dataset loaded. Please load a dataset first."
    
    try:
        code = generate_viz_code(query, state.schema)
        image_path = execute_viz(code, state.global_df)
        
        if "failed" in image_path.lower() or "error" in image_path.lower():
            return f"Visualization failed: {image_path}"
        
        # Generate insights
        try:
            insights = llm_call(f"Describe insights from visualization: {query}\nSchema: {state.schema}")
        except Exception:
            insights = f"Visualization created for: {query}"
        
        # Store result
        last_analysis_result = {
            'query': query,
            'summary': f"Visualization: {insights}",
            'raw_result': f"Chart saved to: {image_path}",
            'code': code,
            'complexity': 'visualization',
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        
        # Open image
        open_image(image_path)
        
        return f"**Visualization Created:**\n{insights}\n\n**File:** {image_path}\n\n**Code:** {code}"
        
    except Exception as e:
        error_msg = f"Visualization error: {str(e)}"
        return error_msg