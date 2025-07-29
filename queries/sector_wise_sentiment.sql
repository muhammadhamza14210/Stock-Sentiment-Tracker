SELECT 
  sector,
  ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
  COUNT(*) AS total_articles
FROM `stock_dataset.stock_sentiment_data`
GROUP BY sector
ORDER BY avg_sentiment DESC;
