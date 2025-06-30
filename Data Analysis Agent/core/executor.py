"""Safe code execution engine."""

import pandas as pd
import numpy as np
from typing import Any
from config.settings import DANGEROUS_PATTERNS

def execute_code(code: str, df: pd.DataFrame) -> Any:
    """Safe code execution."""
    # Security check
    if any(pattern in code.lower() for pattern in DANGEROUS_PATTERNS):
        return "Unsafe code detected"
    
    try:
        safe_builtins = {
            'print': print, 'len': len, 'range': range,
            'min': min, 'max': max, 'sum': sum,
            'sorted': sorted, 'abs': abs, 'round': round,
            'str': str, 'int': int, 'float': float
        }
        context = {'df': df.copy(), 'pd': pd, 'np': np, **safe_builtins}
        
        if '\n' in code or '=' in code:
            exec(code, context)
            result = context.get('df', "Code executed successfully")
        else:
            result = eval(code, context)
        
        return result
    except Exception as e:
        return f"Execution Error: {str(e)}"