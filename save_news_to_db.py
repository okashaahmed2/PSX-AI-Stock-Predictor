import sqlite3
import feedparser
import urllib.parse

# 1. Google News se headlines fetch karne ka function
def fetch_and_save_news():
    raw_query = "Pakistan Stock Exchange"
    encoded_query = urllib.parse.quote(raw_query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-PK&gl=PK&ceid=PK:en"
    
    feed = feedparser.parse(url)
    
    # 2. Database se connect karein
    conn = sqlite3.connect("psx_project.db")
    cursor = conn.cursor()
    
    saved_count = 0
    
    print("Saving news to database...")
    
    for entry in feed.entries:
        title = entry.title
        publisher = entry.source.get('text', 'Unknown')
        link = entry.link
        published_date = entry.published
        
        try:
            # 3. SQL Insert Query (INSERT OR IGNORE duplicate entries ko skip karegi)
            cursor.execute('''
            INSERT OR IGNORE INTO news_headlines (date, title, source, link)
            VALUES (?, ?, ?, ?)
            ''', (published_date, title, publisher, link))
            
            # Agar record successfully insert ho jaye toh count barhayein
            if cursor.rowcount > 0:
                saved_count += 1
                
        except Exception as e:
            print(f"Error saving headline: {e}")
            
    # 4. Changes commit karein aur close karein
    conn.commit()
    conn.close()
    
    print(f"Done! {saved_count} nayi headlines database mein successfully save ho chuki hain.")

# Function ko run karein
if __name__ == "__main__":
    fetch_and_save_news()