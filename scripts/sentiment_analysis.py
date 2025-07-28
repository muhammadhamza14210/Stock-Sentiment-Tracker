from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER analyzer once
analyzer = SentimentIntensityAnalyzer()

def analyze_article_sentiment(article):
    """
    Takes one article dict, adds sentiment_score and sentiment_label.
    """
    text = f"{article.get('title', '')} {article.get('summary', '')}"
    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.05:
        label = "positive"
    elif score <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    article["sentiment_score"] = round(score, 4)
    article["sentiment_label"] = label
    return article

def analyze_all_articles(articles):
    """
    Takes a list of article dicts, returns with sentiment scores.
    """
    return [analyze_article_sentiment(article) for article in articles]