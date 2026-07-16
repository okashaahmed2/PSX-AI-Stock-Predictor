import sqlite3
import pandas as pd

# Database se connect karein
conn = sqlite3.connect("psx_project.db")

# Dono tables ka data pandas dataframe mein load karein
df_stocks = pd.read_sql_query("SELECT * FROM stock_prices LIMIT 5", conn)
df_news = pd.read_sql_query("SELECT * FROM news_headlines LIMIT 5", conn)

conn.close()

print("--- Database Stock Table (First 5 Rows) ---")
print(df_stocks)
print("\n--- Database News Table (First 5 Rows) ---")
print(df_news)