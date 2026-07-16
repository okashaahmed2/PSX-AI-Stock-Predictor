import sqlite3
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# 1. Database se connect karein aur columns add karein (agar pehle se nahi hain)
conn = sqlite3.connect("psx_project.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE news_headlines ADD COLUMN sentiment_score REAL")
    cursor.execute("ALTER TABLE news_headlines ADD COLUMN sentiment_label TEXT")
    conn.commit()
    print("Database columns successfully add ho gaye!")
except sqlite3.OperationalError:
    print("Columns pehle se add hain. Shabaash!")

# 2. Custom VADER Lexicon Setup (Wahi jo humne optimize kiya)
sia = SentimentIntensityAnalyzer()
psx_custom_lexicon = {
    'bull': 2.0, 'bulls': 2.0, 'bullish': 2.5,
    'gains': 2.0, 'gain': 1.5, 'rallies': 2.0, 'rally': 1.5, 'rebound': 1.8, 'rebounds': 1.8,
    'snap': 1.0, 'bear': -2.0, 'bears': -2.0, 'bearish': -2.5,
    'bloodbath': -3.5, 'sheds': -1.5, 'decline': -1.5, 'loses': -1.5, 'rout': -2.5
}
sia.lexicon.update(psx_custom_lexicon)

# 3. Wo headlines uthayein jinka sentiment abhi tak analyze nahi hua (Null hain)
cursor.execute("SELECT id, title FROM news_headlines WHERE sentiment_score IS NULL")
rows = cursor.fetchall()

print(f"Total {len(rows)} un-analyzed headlines mili hain. Chaliye analyze karte hain...")

# 4. Sentiment analyze karke database update karein
updated_count = 0
for row in rows:
    row_id, title = row[0], row[1]
    
    # Sentiment calculate karein
    scores = sia.polarity_scores(title)
    compound_score = scores['compound']
    
    if compound_score >= 0.05:
        label = "POSITIVE"
    elif compound_score <= -0.05:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"
        
    # Database update query
    cursor.execute('''
    UPDATE news_headlines 
    SET sentiment_score = ?, sentiment_label = ? 
    WHERE id = ?
    ''', (compound_score, label, row_id))
    
    updated_count += 1

conn.commit()
conn.close()

print(f"Done! {updated_count} headlines ka sentiment database mein update ho chuka hai!")