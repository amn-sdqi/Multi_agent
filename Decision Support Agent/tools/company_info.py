# tools/company_info.py
import yfinance as yf

def get_company_info(symbol: str) -> str:
    """Returns basic company info as a formatted string."""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        if not info:
            return f"No company info found for symbol: {symbol}"

        name = info.get("longName", "N/A")
        sector = info.get("sector", "N/A")
        market_cap = info.get("marketCap", "N/A")
        summary = info.get("longBusinessSummary", "N/A")

        return (
            f" **Company Name:** {name}\n"
            f" **Sector:** {sector}\n"
            f" **Market Cap:** {market_cap}\n"
            f" **Summary:** {summary}"
        )

    except Exception as e:
        return f" Error retrieving info for {symbol}: {e}"

def get_company_news(symbol: str) -> str:
    """Returns the latest 5 news headlines for a company as a string."""
    try:
        stock = yf.Ticker(symbol)
        news_data = stock.news

        if not news_data:
            return f"No news available for {symbol}."

        headlines = [item.get("title", "No Title") or item.get("headline") or item.get("link")  for item in news_data[:5]]
        return f" Latest News for {symbol}:\n" + "\n".join(f"- {title}" for title in headlines)

    except Exception as e:
        return f" Error fetching news for {symbol}: {e}"
