import pandas as pd
from datetime import datetime

def save_report(df, tickers, retrieved_at, output_path="data/report.txt"):
    with open(output_path, "w") as f:
        f.write("────────────── Summary ──────────────\n")
        f.write(f"Report Generated at: {retrieved_at}\n")
        f.write(f"Tickers Processed: {len(tickers)}\n")
        f.write(f"Total Articles Collected: {len(df)}\n\n")

        if df.empty:
            f.write("No data available to generate insights.\n")
            return

        f.write("────────────── Insights ─────────────\n")

        # Avg sentiment per ticker
        avg_scores = df.groupby("ticker")["sentiment_score"].mean()

        top_bullish = avg_scores.idxmax()
        top_bearish = avg_scores.idxmin()

        f.write(f"\nTop Bullish Ticker: {top_bullish} (avg: {avg_scores[top_bullish]:.3f})\n")
        f.write(f"Top Bearish Ticker: {top_bearish} (avg: {avg_scores[top_bearish]:.3f})\n")

        most_mentioned = df["ticker"].value_counts().idxmax()
        mentions = df["ticker"].value_counts()[most_mentioned]
        f.write(f"Most Mentioned Ticker: {most_mentioned} ({mentions} articles)\n")

def save_leaderboard(df: pd.DataFrame, output_path="data/sentiment_leaderboard.csv"):
    if df.empty:
        print("Skipping leaderboard: no data available.")
        return

    leaderboard = (
        df.groupby("ticker")["sentiment_score"]
        .mean()
        .reset_index()
        .rename(columns={"sentiment_score": "avg_sentiment_score"})
    )
    leaderboard["avg_sentiment_score"] = leaderboard["avg_sentiment_score"].round(3)
    leaderboard = leaderboard.sort_values("avg_sentiment_score", ascending=False)
    leaderboard.to_csv(output_path, index=False)

def save_daily_trend(df: pd.DataFrame, output_path="data/daily_sentiment_trend.csv"):
    if df.empty:
        print("Skipping daily trend: no data available.")
        return

    df["date"] = pd.to_datetime(df["datetime"]).dt.date
    daily_trend = (
        df.groupby(["ticker", "date"])["sentiment_score"]
        .mean()
        .reset_index()
        .rename(columns={"sentiment_score": "avg_daily_sentiment"})
    )
    daily_trend["avg_daily_sentiment"] = daily_trend["avg_daily_sentiment"].round(3)
    daily_trend = daily_trend.sort_values(["ticker", "date"])
    daily_trend.to_csv(output_path, index=False)