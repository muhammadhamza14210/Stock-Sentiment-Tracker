import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load API key
load_dotenv()
NEWS_KEY = os.getenv("NEWS_API")

def fetch_news_articles(ticker, page_size=20, skip_if_empty=True):
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={ticker}&language=en&sortBy=publishedAt&pageSize={page_size}&apiKey={NEWS_KEY}"
    )

    print(f"Fetching news for {ticker}...")
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        print("Error from NewsAPI:", data.get("message"))
        return []

    articles = data.get("articles", [])
    if skip_if_empty and not articles:
        print(f"No articles found for {ticker}, skipping.")
        return None

    rows = []

    for article in articles:
        rows.append({
            "ticker": ticker,
            "datetime": article["publishedAt"],
            "title": article["title"],
            "summary": article["description"],
            "source": article["source"]["name"]
        })

    print(f"Retrieved {len(rows)} articles for {ticker}")
    return rows
