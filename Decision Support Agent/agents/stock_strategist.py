# agents/stock_strategist.py

import os
import logging
import json
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq

# Load env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

# Define a placeholder tool
tool = Tool(
    name="InvestmentAdvisor",
    func=lambda x: x,
    description="Receives a dictionary of market analysis and company research, and recommends which stocks to invest in."
)

# Initialize Agent with max_iterations to prevent infinite loops
agent = initialize_agent(
    tools=[tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True  # This will stop the agent from crashing
)

# Main function to recommend stocks
def recommend_stocks(analysis_data: dict):
    try:
        logger.info("💡 Recommending stocks based on analysis...")
        formatted_input = json.dumps(analysis_data, indent=2)
        
        # ✅ Updated prompt
        prompt = f"""
You're a financial investment strategist.

Below is the structured investment analysis data from market and company analysis:
{formatted_input}

Based on the above data:
- Recommend the top stock(s) to invest in.
- Justify your choice with reasoning.
- Consider market performance, company fundamentals, and risks.
- Be concise and insightful.

🚨 IMPORTANT: End your output with
Final Answer: [TICKER] because [your reasoning]
"""

        return agent.run(prompt)
    
    except Exception as e:
        logger.error(f"❌ Stock recommendation failed: {e}")
        return "Unable to generate stock recommendations at the moment."
