SELECT 
  ticker,
  title,
  sentiment_score,
  price_change_pct,
  DATE(datetime) AS date,
  CASE 
    WHEN sentiment_score > 0.85 AND price_change_pct < 0 THEN "Positive Sentiment, Negative Price"
    WHEN sentiment_score < -0.85 AND price_change_pct > 0 THEN "Negative Sentiment, Positive Price"
    ELSE "Aligned"
  END AS mismatch_flag
FROM `stock_dataset.stock_sentiment_data`
WHERE ABS(sentiment_score) > 0.85
ORDER BY ABS(sentiment_score) DESC;