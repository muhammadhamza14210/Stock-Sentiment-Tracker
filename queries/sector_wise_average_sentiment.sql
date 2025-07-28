SELECT
  sector,
  DATE(datetime) AS date,
  ROUND(AVG(sentiment_score), 3) AS avg_sentiment
FROM
  `stock_dataset.stock_sentiment_data`
GROUP BY
  sector, date
ORDER BY
  date, avg_sentiment DESC

  