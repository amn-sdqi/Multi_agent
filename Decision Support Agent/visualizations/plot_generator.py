# visualizations/plot_generator.py

import yfinance as yf
import plotly.graph_objs as go
import os

def generate_stock_performance_plot(ticker_dict, output_path="output/stock_performance_plot.png"):
    fig = go.Figure()
    
    for ticker, name in ticker_dict.items():
        data = yf.Ticker(ticker).history(period="6mo")
        fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name=name))
    
    fig.update_layout(
        title="📈 6-Month Stock Price Trend",
        xaxis_title="Date",
        yaxis_title="Closing Price (USD)",
        template="plotly_dark"
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_image(output_path)
    return output_path



# ticker_dict = {
#     "AAPL": "Apple",
#     "KO": "Coca Cola"
# }

# # 3. Call plot generator
# plot_path = generate_stock_performance_plot(ticker_dict)

# # 4. Print report and plot info
# print("\n📘 Final Investment Report:\n")
# # print(report)
# print(f"\n🖼️ Plot saved at: {plot_path}")
