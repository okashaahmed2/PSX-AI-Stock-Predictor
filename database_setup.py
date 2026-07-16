import sqlite3

# Fresh connection
conn = sqlite3.connect("psx_project.db")
cursor = conn.cursor()

# 1. Stock Prices Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    ticker TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    UNIQUE(date, ticker)
)
''')

# 2. News Headlines Table with Sentiment Label for FinBERT
cursor.execute('''
CREATE TABLE IF NOT EXISTS news_headlines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    ticker TEXT,
    title TEXT UNIQUE,
    source TEXT,
    link TEXT,
    sentiment_score REAL DEFAULT 0.0,
    sentiment_label TEXT DEFAULT 'NEUTRAL'
)
''')

conn.commit()
conn.close()
print("Database 'psx_project.db' verified and ready!")