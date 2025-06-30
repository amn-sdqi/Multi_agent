# chains/investment_report_chain.py

import logging
from agents.market_analyst import analyze_market
from agents.company_researcher import research_company
from agents.stock_strategist import recommend_stocks
from agents.team_lead import compile_final_report

# ✅ Logging Configuration with Timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def generate_full_report(symbols):
    """
    Chains together multiple agents to generate a final investment report.

    Args:
        symbols (list of str): Stock tickers like ['AAPL', 'GOOGL']

    Returns:
        str: Final compiled investment report or an error message.
    """

    logger.info("⏳ Starting investment report generation...")

    # ✅ Input validation
    if not isinstance(symbols, list) or not all(isinstance(s, str) for s in symbols):
        logger.error("❌ Invalid input. Expected a list of stock ticker strings.")
        return "❌ Invalid input: Expected a list of ticker symbols (e.g., ['AAPL', 'GOOGL'])."

    if len(symbols) < 2:
        logger.warning("⚠️ Less than two tickers provided.")
        return "⚠️ Please provide at least two company tickers to generate a comparative investment report."

    # ✅ Step 1: Market Analysis
    try:
        market_analysis = analyze_market(symbols)
        logger.info("✅ Market analysis completed.")
    except Exception as e:
        logger.error(f"❌ Error during market analysis: {e}")
        return f"❌ Error during market analysis: {e}"

    # ✅ Step 2: Company Research (one by one)
    company_analyses = {}
    for symbol in symbols:
        try:
            company_analyses[symbol] = research_company(symbol)
            logger.info(f"📊 Company research completed for {symbol}.")
        except Exception as e:
            company_analyses[symbol] = f"⚠️ Error analyzing {symbol}: {e}"
            logger.warning(f"⚠️ Error analyzing {symbol}: {e}")

    # ✅ Step 3: Stock Recommendations
    try:
        recommendation_input = {
        "market_analysis": market_analysis,
        "company_profiles": company_analyses
        }
        recommendations = recommend_stocks(recommendation_input)
        # recommendations = recommend_stocks(symbols)
        logger.info("✅ Stock recommendations generated.")
    except Exception as e:
        logger.error(f"❌ Error generating stock recommendations: {e}")
        return f"❌ Error generating stock recommendations: {e}"

    # ✅ Step 4: Compile Final Report
    try:
        final_report = compile_final_report(market_analysis, company_analyses, recommendations)
        logger.info("✅ Final investment report compiled successfully.")
        return final_report
    except Exception as e:
        logger.error(f"❌ Error compiling final report: {e}")
        return f"❌ Error compiling final report: {e}"
