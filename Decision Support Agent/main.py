import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from visualizations.plot_generator import generate_stock_performance_plot
from query_parser import extract_valid_companies
from tools.ticker_lookup import TickerLookupTool
from chain.investment_report_chain import generate_full_report
import ast

def main(user_query):
    # Step 1: Extract string response from model
    raw_response = extract_valid_companies(user_query)

    # Step 2: Try parsing response into a list
    company_list = None
    try:
        if raw_response.startswith("[") and raw_response.endswith("]"):
            parsed = ast.literal_eval(raw_response)
            if isinstance(parsed, list):
                company_list = [c.strip() for c in parsed]  # Clean company names
    except Exception as e:
        print(f"[QueryParser Error] {e}")

    # Step 3: If parsing was successful, use the ticker tool
    if company_list:
        print(f"\n Valid Companies Found: {company_list}")
        company_string = ", ".join(company_list)

        ticker_tool = TickerLookupTool()
        ticker_result = ticker_tool._run(company_string)

        print("\n Ticker Result:", ticker_result)

        # Step 3: If ticker_result is valid, generate report
        if "Invalid company names" not in ticker_result:
            tickers = [t.strip() for t in ticker_result.split(",")]
            # 1. Generate investment report
            report = generate_full_report(tickers)

            # 2. Dynamically map tickers to names
            ticker_dict = dict(zip(tickers, company_list))

            # 3. Call plot generator
            plot_path = generate_stock_performance_plot(ticker_dict)

            # 4. Print report and plot info
            print("\n Final Investment Report:\n")
            print(report)
            print(f"\n Plot saved at: {plot_path}")

        else:
            print("\n Ticker lookup failed. Please re-enter with valid company names.")


    else:
        # If parsing failed, just print the raw response
        print("\n Invalid query or not enough valid company names.")
        print("Raw LLM Response:", raw_response)



if __name__ == "__main__":
    user_query = input("Enter your investment query: ")
    main(user_query)




