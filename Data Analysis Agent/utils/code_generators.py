"""Code generation utilities."""

import re
from core.llm import llm_call

def generate_code(query: str, schema: str) -> str:
    """Generate pandas code."""
    prompt = f"""
Convert the natural language query into correct and safe pandas code.

Rules:
1. Use 'df' as the DataFrame variable.
2. Return ONLY valid Python code (no explanations, markdown, or ``` blocks).
3. Do NOT use '.loc' after 'groupby()', 'mean()', or any chained statistical operation.
4. Filter rows using boolean indexing BEFORE applying 'groupby' or aggregations.
5. For numeric column operations, use: df.select_dtypes(include=['number'])
6. Avoid using 'print()' – just return the code lines.

Schema: {schema}
Query: "{query}"

Generate only the pandas code:
"""

    
    try:
        result = llm_call(prompt)
        code = re.sub(r'^```(?:python)?\s*', '', result).rstrip('`')
        return code.replace("print(", "# print(").strip()
    except Exception:
        # Simple fallbacks
        query_lower = query.lower()
        fallbacks = {
            'head': "df.head()",
            'tail': "df.tail()",
            'info': "df.info()",
            'describe': "df.describe()",
            'shape': "df.shape",
            'columns': "df.columns"
        }
        for key, code in fallbacks.items():
            if key in query_lower:
                return code
        return "df.head()"

def generate_viz_code(query: str, schema: str) -> str:
    """Generate visualization code."""
    prompt = f"""
Create matplotlib/seaborn visualization code. Rules:
1. Use 'df' as dataframe
2. No plt.show()
3. Return only code
4. For correlation matrix: use sns.heatmap(df.select_dtypes(include=['number']).corr(), annot=True)
5. If the user asks for a subplot, generate a matplotlib subplot (using plt.subplots) instead of a single plot
6. Do not use plt.figure when generating subplot use plt.subplots
7. Always handle numeric data properly

Schema: {schema}
Query: "{query}"

Generate visualization code:
"""
    
    try:
        result = llm_call(prompt)
        code = result.strip()
        
        # Clean code
        if '```' in code:
            parts = code.split('```')
            if len(parts) >= 3:
                code = parts[1]
                if code.startswith('python\n'):
                    code = code[7:]
            else:
                code = re.sub(r'^```(?:python)?\s*', '', code)
        
        code = code.strip('`').strip()
        
        # Remove explanatory patterns
        explanatory_patterns = [
            r'^Here is.*?:\s*',
            r'^The.*?code.*?:\s*',
            r'^```.*?\n',
            r'\n```.*?$'
        ]
        
        for pattern in explanatory_patterns:
            code = re.sub(pattern, '', code, flags=re.IGNORECASE | re.MULTILINE)
        
        return code.strip()
    except Exception:
        return "plt.figure(figsize=(10,6))\ndf.hist()\nplt.title('Data Distribution')"

def generate_summary(query: str, result: str, code: str = "") -> str:
    """Generate result summary."""
    prompt = f"""
Provide insights about this analysis result (2-3 sentences):

Query: {query}
Result: {str(result)[:500]}
Code: {code}

Summary:
"""
    
    try:
        return llm_call(prompt)
    except Exception:
        return f"Analysis completed for: {query}"