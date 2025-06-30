# tools/ticker_lookup.py

from langchain.tools import BaseTool
import yfinance as yf
import requests
from functools import lru_cache
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@lru_cache(maxsize=128)
def search_yahoo_ticker(query: str) -> Optional[str]:
    url = "https://query2.finance.yahoo.com/v1/finance/search "
    params = {"q": query, "quotes_count": 1}
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if data.get("quotes"):
            return data["quotes"][0]["symbol"]
    except Exception as e:
        logger.error(f"Yahoo search error for '{query}': {e}")
    return None


class TickerLookupTool(BaseTool):
    name: str = "ticker_lookup"
    description: str = "Finds best matching ticker symbols for given company names."

    def _run(self, query: str, run_manager=None) -> str:
        names = [name.strip() for name in query.split(",")]
        
        # Step 1: Validate input
        if not names:
            return "Please provide at least one company name."
        
        # Step 2: Resolve tickers
        tickers = []
        invalid_names = []
        for name in names:
            try:
                # Try yfinance first
                search = yf.Search(name, max_results=1)
                if search.quotes:
                    tickers.append(search.quotes[0]["symbol"])
                    continue

                # Fallback to Yahoo search
                ticker = search_yahoo_ticker(name)
                if ticker:
                    tickers.append(ticker)
                    continue

                # Log warning for invalid names
                logger.warning(f"No ticker found for '{name}'. Skipping...")
                invalid_names.append(name)
            except Exception as e:
                logger.error(f"Error finding ticker for '{name}': {str(e)}")
                invalid_names.append(name)

        # Step 3: Handle invalid names
        if invalid_names:
            return f"Invalid company names: {', '.join(invalid_names)}. Please try again."

        # Step 4: Return resolved tickers
        return ", ".join(tickers)

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async version not implemented.")
