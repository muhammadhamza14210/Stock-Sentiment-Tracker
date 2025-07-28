SELECT
  ticker,
  COUNT(*) AS news_count,
  ROUND(STDDEV(sentiment_score), 4) AS sentiment_volatility
FROM
  `stock_dataset.stock_sentiment_data`
GROUP BY
  ticker
ORDER BY
  sentiment_volatility DESC
LIMIT 10;
