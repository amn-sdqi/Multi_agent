# app.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from langchain_core.tools import tool
import tempfile

from analyzer import load_csv_texts, load_json_texts, analyze_texts
from summarize import summarize_results

app = FastAPI(title="Sentiment & Emotion Agent")


@tool(return_direct=True)
async def sentiment_init(
    file: UploadFile = File(...),
    file_type: str = Form(...),  # 'csv' or 'json'
    jq_schema: str = Form(".messages[].review"),  # Optional for JSON
):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()

        if file_type == "csv":
            texts = load_csv_texts(tmp.name)
        elif file_type == "json":
            texts = load_json_texts(tmp.name, jq_schema=jq_schema)
        else:
            return JSONResponse(
                status_code=400, content={"error": "Unsupported file_type"}
            )

    results = analyze_texts(texts)
    summary = summarize_results(results)

    return {"summary": summary, "results": results}
