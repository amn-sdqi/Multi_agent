"""Dataset loading utilities."""

import pandas as pd
import json
from config.settings import ENCODING_OPTIONS

def load_dataset(path: str) -> pd.DataFrame:
    """Load dataset with encoding detection."""
    if path.endswith(".csv"):
        for enc in ENCODING_OPTIONS:
            try:
                return pd.read_csv(path, encoding=enc)
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Could not decode {path} with common encodings.")
    elif path.endswith(".json"):
        return pd.read_json(path)
    else:
        raise ValueError("Unsupported file type")

def generate_schema(df: pd.DataFrame) -> str:
    """Generate schema information."""
    return json.dumps({
        "shape": list(df.shape),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }, indent=2)