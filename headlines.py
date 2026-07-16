import feedparser
import urllib.parse

# 1. Search query define karein
raw_query = "Pakistan Stock Exchange"

# 2. Spaces aur special characters ko URL-safe format mein convert karein
# (Jaise "Pakistan Stock Exchange" ban jayega "Pakistan%20Stock%20Exchange")
encoded_query = urllib.parse.quote(raw_query)

# 3. Google News RSS Feed URL banayein
url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-PK&gl=PK&ceid=PK:en"

# 4. Feed ko parse (read) karein
feed = feedparser.parse(url)

print(f"--- Latest News & Headlines for: {raw_query} --- \n")

# 5. Agar feed mein articles hain toh top 5 show karein
if feed.entries:
    for index, entry in enumerate(feed.entries[:5], 1):
        title = entry.title
        publisher = entry.source.get('text', 'Unknown')
        link = entry.link
        published_date = entry.published
        
        print(f"{index}. Title: {title}")
        print(f"   Source: {publisher}")
        print(f"   Date: {published_date}")
        print(f"   Link: {link}")
        print("-" * 60)
else:
    print("Koi news nahi mili. Net connection check karein ya query badlein.")