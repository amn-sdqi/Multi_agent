# analyzer.py
from langchain_community.document_loaders import CSVLoader, JSONLoader
from agent_core import analysis_tool


def analyze_texts(texts):
    results = [analysis_tool.invoke(text) for text in texts]
    return results


def load_csv_texts(file_path):
    loader = CSVLoader(file_path=file_path)
    docs = loader.load()
    return [doc.page_content for doc in docs]


def load_json_texts(file_path, jq_schema):
    loader = JSONLoader(file_path=file_path, jq_schema=jq_schema)
    docs = loader.load()
    return [doc.page_content for doc in docs]
