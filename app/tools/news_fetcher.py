import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
from datetime import datetime, timedelta

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "demo")

def get_recent_news_summaries(topic: str, max_results: int = 5) -> list:
    """
    Fetches recent news headlines and short summaries about a topic using NewsAPI.
    """
    # Use past 7 days as the default window
    from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={topic}&from={from_date}&sortBy=publishedAt&language=en&pageSize={max_results}&apiKey=f9e89899691546298c452cd3ebfb9453"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("status") != "ok":
            print(f"[NewsAPI Error] {data.get('message')}")
            return [f"Error: {data.get('message')}"]

        articles = data.get("articles", [])
        print(f"[NewsAPI] Found {len(articles)} articles for topic '{topic}'")
        summaries = [
            f"{article['title']} — {article['description']}"
            for article in articles
            if article.get("description")
        ]

        return summaries or ["No relevant articles found."]

    except Exception as e:
        print(f"[News Fetch Error] {e}")
        return ["Error fetching news."]
