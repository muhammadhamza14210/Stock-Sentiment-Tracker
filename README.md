# 📊 Stock Sentiment Tracker

A full-stack, end-to-end project that scrapes real-time financial news, performs sentiment analysis, and correlates results with stock price movements all visualized in Looker Studio via BigQuery.

---

## 🚀 Project Overview

This project simulates a real-world data pipeline that:

- Collects stock market news via API
- Performs **NLP-based sentiment analysis**
- Fetches live stock prices
- Calculates **daily average sentiment**, **price change %**, and **leaderboards**
- Uploads the final datasets to **Google BigQuery**
- Visualizes everything with a **Looker Studio dashboard**
- Runs automatically with **Docker & GitHub Actions**

---

## 🧱 Tech Stack

| Layer            | Tools / Libraries                |
| ---------------- | -------------------------------- |
| **Language**     | Python 3.10, SQL                 |
| **Data Sources** | NewsAPI, Yahoo Finance           |
| **Sentiment**    | VADER (NLTK)                     |
| **Cloud**        | Google Cloud Platform (BigQuery) |
| **Automation**   | Docker, GitHub Actions           |
| **Viz**          | Looker Studio                    |

---

## 📁 Directory Structure
```bash
├── .github/workflows/
│ ├── main.yml
├── data/       # Final CSV outputs
│ ├── daily_sentiment_trend.csv
│ ├── final_data.csv
│ ├── report.txt
│ ├── sentiment_leaderboard.csv 
├── scripts/
│ ├── fetch_stock_data.py
│ ├── fetch_stock_news.py
│ ├── sentiment_analysis.py
│ ├── postprocessing.py
│ └── gcp_upload.py
├── utils/
│ └── constants.py # Sector mappings
├── main.py
├── Dockerfile
├── requirements.txt
└── .env
```

## ⚙️ Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/stock-sentiment-tracker.git
cd stock-sentiment-tracker
```

### 2. Set ENV Variables

```bash
NEWS_API_KEY=your_newsapi_key
```

### 3. Add GCP Credentials

- Download your service account key as JSON from Google Cloud and rename it: ```gcp_key.json```

### 4. Docker Build and Run

```bash
docker build -t stock-sentiment-tracker .

docker run --env-file .env -v $(pwd)/gcp_key.json:/app/gcp_key.json stock-sentiment-tracker
```