# agents/team_lead.py

from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

# Optional: Tool definition can be removed if not used by LangChain agent
tool = Tool(
    name="ReportCompiler",
    func=lambda x: x,
    description="Compiles market analysis, company analysis, and stock recommendations into a user-friendly investment report."
)

agent = initialize_agent([tool], llm, agent="zero-shot-react-description", verbose=True)

def compile_final_report(market_analysis, company_analyses, recommendations):
    """
    Compiles final investment report from all agent outputs.

    Args:
        market_analysis (str): Output from market analyst
        company_analyses (dict): Output from company researcher
        recommendations (str): Output from stock strategist

    Returns:
        str: Final formatted investment report
    """
    
    prompt = f"""
You are the Team Lead AI for Investment Strategy. Your job is to compile a final **professional and user-friendly** investment report using the following input data:

=========================
📈 Market Analysis:
{market_analysis}

🏢 Company Analyses:
{company_analyses}

🧠 Stock Recommendations:
{recommendations}
=========================

Now, based on the above, write a structured and well-formatted investment report that includes:

1. **📊 Summary of Stock Performance** (brief and comparative)
2. **🧩 Key Company Insights** (1–2 lines for each company)
3. **⚖️ Risk–Reward Assessment** (mention if data is missing or unclear)
4. **✅ Final Recommendation**:
   - Top 1–2 stock(s) to invest in
   - Justification based on the data
5. **Rank stocks** (from best to worst recommendation)
    like : Apple > Microsoft > Google 
🪄 Please format the response clearly using **headings**, **bullet points**, and **rankings if relevant**. Keep the tone professional and informative, suitable for business stakeholders.

Output should feel like a polished executive summary. Be concise but insightful.
"""

    return agent.run(prompt)
