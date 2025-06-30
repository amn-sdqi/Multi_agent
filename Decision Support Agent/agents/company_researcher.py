# agents/company_researcher.py

import os
from dotenv import load_dotenv
import logging
from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from tools.company_info import get_company_info, get_company_news

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

# Define Tools
tools = [
    Tool(
        name="CompanyInfo",
        func=lambda x: str(get_company_info(x)),
        description="Returns basic company profile information such as name, sector, market cap, and a brief summary."
    ),
    Tool(
        name="CompanyNews",
        func=lambda x: str(get_company_news(x)),
        description="Returns the 5 latest news headlines for a company using its stock ticker."
    )
]

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="structured-chat-zero-shot-react-description",
    max_iterations=4,  # Add this to prevent infinite retries
    verbose=True
)

# Main callable function
def research_company(symbol: str) -> str:
    try:
        logger.info(f"🔍 Researching company: {symbol}")
        return agent.invoke(f"Provide a detailed fundamental and recent news analysis for the stock ticker: {symbol}")
    except Exception as e:
        logger.error(f"❌ Failed to research company {symbol}: {e}")
        return f"Could not retrieve information for {symbol}."
