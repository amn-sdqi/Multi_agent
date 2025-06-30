import pandas as pd
import json

def extract_schema_preview(df: pd.DataFrame) -> dict:
    """Extract schema information and sample rows from DataFrame"""
    return {
        "shape": list(df.shape),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "sample_rows": df.head().to_dict(orient='records')
    }