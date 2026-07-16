import sqlite3
import yfinance as yf

def fetch_and_save_stocks():
    # Reverted to active Yahoo extension format
    ticker_symbol = "SYS.KA"
    print(f"Fetching stock data for {ticker_symbol}...")
    
    stock = yf.Ticker(ticker_symbol)
    df = stock.history(period="1mo", interval="1d")
    
    conn = sqlite3.connect("psx_project.db")
    cursor = conn.cursor()
    
    saved_count = 0
    
    for index, row in df.iterrows():
        date_str = index.strftime('%Y-%m-%d')
        open_val = round(row['Open'], 2)
        high_val = round(row['High'], 2)
        low_val = round(row['Low'], 2)
        close_val = round(row['Close'], 2)
        volume_val = int(row['Volume'])
        
        try:
            cursor.execute('''
            INSERT OR IGNORE INTO stock_prices (date, ticker, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (date_str, ticker_symbol, open_val, high_val, low_val, close_val, volume_val))
            
            if cursor.rowcount > 0:
                saved_count += 1
                
        except Exception as e:
            print(f"Error saving row for {date_str}: {e}")
            
    conn.commit()
    conn.close()
    print(f"Successfully saved {saved_count} new trading days into database!")

if __name__ == "__main__":
    fetch_and_save_stocks()