SELECT 
  sentiment_label,
  COUNTIF(price_change_pct > 2) AS strong_gain,
  COUNTIF(price_change_pct BETWEEN 0 AND 2) AS mild_gain,
  COUNTIF(price_change_pct < 0) AS drop
FROM `stock-analysis-467310.stock_dataset.stock_sentiment_data`
GROUP BY sentiment_label;
