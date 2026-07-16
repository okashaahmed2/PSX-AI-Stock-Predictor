import sqlite3
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# NLTK Lexicon download karein
nltk.download('vader_lexicon')

# 1. Sentiment Analyzer initialize karein
sia = SentimentIntensityAnalyzer()

# 2. Pakistan Stock Exchange ke liye CUSTOM WORDS define karein
# Hum dictionary mein naye words add kar rahe hain aur unko scores de rahe hain
psx_custom_lexicon = {
    'bull': 2.0,
    'bulls': 2.0,
    'bullish': 2.5,
    'gains': 2.0,
    'gain': 1.5,
    'rallies': 2.0,
    'rally': 1.5,
    'rebound': 1.8,
    'rebounds': 1.8,
    'snap': 1.0,           # 'snap losing' ka 'snap'
    'bear': -2.0,
    'bears': -2.0,
    'bearish': -2.5,
    'bloodbath': -3.5,
    'sheds': -1.5,
    'decline': -1.5,
    'loses': -1.5,
    'rout': -2.5
}

# In custom words ko VADER ki default dictionary mein update (merge) karein
sia.lexicon.update(psx_custom_lexicon)

# 3. Database se headlines read karein
conn = sqlite3.connect("psx_project.db")
cursor = conn.cursor()
cursor.execute("SELECT title FROM news_headlines LIMIT 5")
rows = cursor.fetchall()
conn.close()

print("--- Analyzing Sentiment with IMPROVED Financial VADER --- \n")

# 4. Sentiment analyze karein
for index, row in enumerate(rows, 1):
    headline = row[0]
    
    # Custom weights ke sath sentiment calculate hoga
    scores = sia.polarity_scores(headline)
    compound_score = scores['compound']
    
    if compound_score >= 0.05:
        sentiment = "POSITIVE 🟢"
    elif compound_score <= -0.05:
        sentiment = "NEGATIVE 🔴"
    else:
        sentiment = "NEUTRAL ⚪"
        
    print(f"{index}. Headline: {headline}")
    print(f"   Compound Score: {compound_score}")
    print(f"   Sentiment: {sentiment}")
    print("-" * 60)