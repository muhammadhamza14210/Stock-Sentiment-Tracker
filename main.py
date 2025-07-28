import os
import pandas as pd
from datetime import datetime, timezone
from scripts.fetch_stock_data import fetch_stock_data
from scripts.fetch_stock_news import fetch_news_articles
from scripts.sentiment_analysis import analyze_all_articles
from scripts.postprocessing import save_report, save_leaderboard, save_daily_trend
from scripts.gcp_upload import upload_csv_to_bigquery
from utils.constants import SECTOR_MAP

tickers = list(SECTOR_MAP.keys())

def get_latest_stock_price(stock_data):
    if not stock_data:
        return None
    return stock_data[0]["price"]

def clean_text(text):
    if not text:
        return ""
    return text.replace('\n', ' ').replace('\r', '').replace('\xa0', ' ').strip()

def get_price_on_date(prices, target_time):
    """
    Finds the closest price on or before the given target_time.
    """
    prices = sorted(prices, key=lambda x: x["datetime"])
    for entry in reversed(prices):
        if entry["datetime"] <= target_time:
            return entry["price"]
    return None

def calculate_price_change_pct(prices, article_time, latest_price, days=1):
    """
    Calculates price change vs 'days' before article time.
    """
    target_time = article_time - pd.Timedelta(days=days)
    past_price = get_price_on_date(prices, target_time)

    if past_price is None or past_price == 0:
        return None
    
    return round((latest_price - past_price) / past_price * 100, 2)

def main():
    print("Starting Combined Sentiment Tracker\n")
    os.makedirs("data", exist_ok=True)

    combined_rows = []

    retrieved_at = datetime.now(timezone.utc).isoformat()

    for ticker in tickers:
        print(f"\nProcessing {ticker}...")

        # 1. Fetch stock data
        stock_data = fetch_stock_data(ticker)
        latest_price = get_latest_stock_price(stock_data)

        # 2. Fetch news
        news_data = fetch_news_articles(ticker)

        # 3. Analyze sentiment
        news_with_sentiment = analyze_all_articles(news_data)

        # 4. Combine everything
        for article in news_with_sentiment:
            article_time = pd.to_datetime(article["datetime"])
            price_change_pct = calculate_price_change_pct(stock_data, article_time, latest_price, days=1)

            combined_rows.append({
                "ticker": ticker,
                "datetime": article["datetime"],
                "title": clean_text(article["title"]),
                "summary": clean_text(article["summary"]),
                "source": clean_text(article["source"]),
                "sector": SECTOR_MAP.get(ticker, "Unknown"),
                "sentiment_score": article["sentiment_score"],
                "sentiment_label": article["sentiment_label"],
                "latest_price": round(latest_price, 2),
                "retrieved_at": retrieved_at,
                "price_change_pct": price_change_pct
            })

    # Save
    df = pd.DataFrame(combined_rows)
    df.to_csv("data/final_data.csv", index=False)
    save_report(df, tickers, retrieved_at)
    save_leaderboard(df)
    save_daily_trend(df)

    print("\n Combined data saved to data/final_data.csv")
    print("\n Uploading to BigQuery...")
    upload_csv_to_bigquery("data/final_data.csv", "stock_sentiment_data")
    upload_csv_to_bigquery("data/sentiment_leaderboard.csv", "sentiment_leaderboard")
    upload_csv_to_bigquery("data/daily_sentiment_trend.csv", "daily_sentiment_trend")
    
if __name__ == "__main__":
    main()
