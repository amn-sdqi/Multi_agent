# tools/stock_data.py

import yfinance as yf
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_stock_performance(symbols: list[str]) -> dict:
    """
    Fetches 6-month performance for given symbols.

    Args:
        symbols (list): List of ticker symbols

    Returns:
        dict: {symbol: % change from 6 months ago to today}
    """
    performance = {}

    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="6mo")

            if hist.empty or 'Close' not in hist.columns:
                logger.warning(f" No data found for symbol: {symbol}")
                continue

            # Calculate % change from 6 months ago to now
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            pct_change = ((end_price - start_price) / start_price) * 100

            performance[symbol] = round(pct_change, 2)

        except Exception as e:
            logger.error(f" Error fetching data for {symbol}: {e}")

    if not performance:
        logger.warning(" No valid performance data returned for any symbol.")

    return performance
