# agent_core.py
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from transformers import pipeline
import os
from pydantic import SecretStr
load_dotenv()  
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=SecretStr(GOOGLE_API_KEY) if GOOGLE_API_KEY else None)
sentiment_pipeline = pipeline("sentiment-analysis")
emotion_pipeline = pipeline(
    "text-classification", model="boltuix/bert-emotion", top_k=1
)


@tool(return_direct=True)
def analysis_tool(text: str) -> dict:
    
    """
    Analyze the input text and return sentiment + primary emotion.
    """
    
    sentiment = list(sentiment_pipeline(text))[0]
    emotion = list(emotion_pipeline(text))[0]
    return {
        "Sentiment": {"label": sentiment["label"]},
        "Emotion": {"label": emotion[0]["label"]},
    }


agent = llm.bind_tools([analysis_tool]) # type: ignore
