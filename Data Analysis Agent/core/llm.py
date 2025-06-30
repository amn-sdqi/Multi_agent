"""LLM initialization and utilities."""

from langchain_groq import ChatGroq
from config.settings import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE

# Initialize LLM
llm = ChatGroq(
    temperature=LLM_TEMPERATURE,
    model=LLM_MODEL,
    api_key=GROQ_API_KEY
)

def get_llm():
    """Get the initialized LLM instance."""
    return llm

def llm_call(prompt: str) -> str:
    """Make a call to the LLM."""
    response = llm.invoke(prompt)
    return response.content.strip()