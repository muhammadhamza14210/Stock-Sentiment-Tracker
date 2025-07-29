SELECT 
  ticker,
  ROUND(CORR(sentiment_score, price_change_pct), 3) AS sentiment_price_corr
FROM `stock_dataset.stock_sentiment_data`
WHERE DATE(retrieved_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY ticker
ORDER BY sentiment_price_corr DESC
LIMIT 10;
