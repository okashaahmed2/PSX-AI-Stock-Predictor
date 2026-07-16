import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# 1. Database se connection
conn = sqlite3.connect("psx_project.db")

# --- IMPORTANT FIX: Kisi ek specific stock ka data load karein ---
# Abhi hum Systems Limited (SYS.KA) par model test kar rahe hain
target_ticker = "SYS.KA" 

# Sirf is target ticker ki prices load karein
df_stocks = pd.read_sql_query("""
    SELECT date, close, volume FROM stock_prices 
    WHERE ticker = ?
""", conn, params=(target_ticker,))

# Is target ticker ki news sentiment load karein
df_sentiment = pd.read_sql_query("""
    SELECT date(date) as date, AVG(sentiment_score) as avg_sentiment 
    FROM news_headlines 
    WHERE ticker = ?
    GROUP BY date(date)
""", conn, params=(target_ticker,))

conn.close()

if df_stocks.empty:
    print(f"❌ Error: Database mein {target_ticker} ka koi data nahi mila! Dashboard khol kar pehle 'Fetch Live Data' click karein.")
else:
    # 2. Dono datasets ko Date par Merge karein
    df = pd.merge(df_stocks, df_sentiment, on="date", how="left")
    df['avg_sentiment'] = df['avg_sentiment'].fillna(0.0)

    # Sort by date essential hai sequence trading ke liye
    df = df.sort_values('date').reset_index(drop=True)

    # --- ROLLING SENTIMENT FEATURES ---
    df['sentiment_ma3'] = df['avg_sentiment'].rolling(window=3, min_periods=1).mean()
    df['sentiment_ma7'] = df['avg_sentiment'].rolling(window=7, min_periods=1).mean()

    print(f"\n--- Cleaned Data Sample for {target_ticker} with Sentiment MAs ---")
    print(df[['date', 'close', 'avg_sentiment', 'sentiment_ma3', 'sentiment_ma7']].tail())

    # 3. Feature Engineering (Shift dynamic to avoid leakage)
    df['prev_close'] = df['close'].shift(1)
    df['prev_volume'] = df['volume'].shift(1)
    df['prev_sentiment'] = df['avg_sentiment'].shift(1)
    df['prev_sentiment_ma3'] = df['sentiment_ma3'].shift(1)
    df['prev_sentiment_ma7'] = df['sentiment_ma7'].shift(1)

    # Drop NaN values jo shift ki wajah se pehli row mein aati hain
    df = df.dropna().reset_index(drop=True)

    # Features (X) aur Target (y) select karein
    feature_cols = ['prev_close', 'prev_volume', 'prev_sentiment', 'prev_sentiment_ma3', 'prev_sentiment_ma7']
    X = df[feature_cols]
    y = df['close']

    # 4. Train-Test Split (80% training, 20% testing - shuffle=False sequence ke liye)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # 5. Model Training
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 6. Predictions aur Evaluation
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    print("\n--- Model Evaluation ---")
    print(f"Mean Absolute Error (MAE): Rs. {mae:.2f}")

    # 7. Next Day Prediction DataFrame
    latest_features_df = pd.DataFrame([{
        'prev_close': df['close'].iloc[-1],
        'prev_volume': df['volume'].iloc[-1],
        'prev_sentiment': df['avg_sentiment'].iloc[-1],
        'prev_sentiment_ma3': df['sentiment_ma3'].iloc[-1],
        'prev_sentiment_ma7': df['sentiment_ma7'].iloc[-1]
    }])

    predicted_next_price = model.predict(latest_features_df)[0]

    print(f"\nPredicted Next Day Closing Price: Rs. {predicted_next_price:.2f}")
    print(f"Last Known Closing Price: Rs. {df['close'].iloc[-1]:.2f}")