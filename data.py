import yfinance as yf

# Try the standard root extension for Karachi Stock Exchange
ticker_symbol = "ENGRO.KA"

print(f"Testing Live Data Fetch for: {ticker_symbol}...")
stock = yf.Ticker(ticker_symbol)

# Try fetching with a different period to bypass cache (e.g., 1 month)
data = stock.history(period="1mo")

print("\n--- Engro Stock Data ---")
if data.empty:
    print("❌ Standard symbol failed. Let's try alternative bypass...")
    # Alternative bypass try
    stock_alt = yf.Ticker("ENGRO.K")
    data_alt = stock_alt.history(period="1mo")
    if data_alt.empty:
        print("❌ Alternative failed too. Proceed to Solution 2.")
    else:
        print(data_alt.tail())
else:
    print(data.tail())