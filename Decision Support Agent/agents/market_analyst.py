# agents/market_analyst.py

import os
import logging
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from tools.stock_data import fetch_stock_performance

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # correct typo if needed
    api_key=os.getenv("GROQ_API_KEY")
)

# Define a tool function instead of lambda
def stock_performance_tool(input_text: str) -> str:
    try:
        symbols = [symbol.strip() for symbol in input_text.split(",") if symbol.strip()]
        if not symbols:
            return "❌ No valid stock symbols provided."
        result = fetch_stock_performance(symbols)
        return str(result)
    except Exception as e:
        logger.error(f"❌ Error in stock_performance_tool: {e}")
        return "❌ Failed to fetch stock performance. Please try again."

# Define tool
tool = Tool(
    name="StockPerformanceFetcher",
    func=stock_performance_tool,
    description="Fetches and compares the 6-month performance of given stock symbols."
)

# Optional: Use memory for follow-up investment insights
memory = ConversationBufferMemory(memory_key="chat_history")

def get_market_agent():
    return initialize_agent(
        tools=[tool],
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True,
        max_iterations=4,  # Limits steps to avoid loops
        memory=memory
    )

# Main function to analyze market
def analyze_market(symbols: list[str]) -> str:
    agent = get_market_agent()

    query = f"Compare the 6-month performance of these stocks: {', '.join(symbols)}"
    logger.info(f"📊 Analyzing Market: {query}")

    try:
        response = agent.run(query)
        return response
    except Exception as e:
        logger.error(f"❌ Agent failed during market analysis: {e}")
        return "❌ Market analysis failed. Please try again later."
