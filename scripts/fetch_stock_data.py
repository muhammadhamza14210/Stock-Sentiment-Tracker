import yfinance as yf
from datetime import datetime

def fetch_stock_data(ticker, interval="60m", period="5d"):
    print(f"Fetching Yahoo Finance data for {ticker}...")

    try:
        df = yf.download(ticker, interval=interval, period=period, progress=False, auto_adjust=False)
        if df.empty:
            print(f"No data found for {ticker}")
            return []

        rows = []
        for idx, row in df.iterrows():
            rows.append({
                "ticker": ticker,
                "datetime": idx.to_pydatetime(),
                "price": float(row["Open"].item()),     
                "volume": int(row["Volume"].item()),  
            })

        print(f"Retrieved {len(rows)} records for {ticker}")
        return rows

    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
        return []