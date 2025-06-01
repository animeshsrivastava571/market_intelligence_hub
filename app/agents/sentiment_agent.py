# app/agents/sentiment_agent.py

from app.core.state import AgentState
from app.tools.sentiment_model import get_sentiment_score

def sentiment_agent(state: AgentState) -> AgentState:
    print("🧠 Running Sentiment Agent...")

    insights = state.get("news_insights", [])
    scores = []

    if insights:
        print("📰 Analyzing sentiment over news articles...")
        for article in insights:
            scores.append(get_sentiment_score(article))
    else:
        print("⚠️ No news_insights found, analyzing query string directly.")
        scores.append(get_sentiment_score(state.get("query", "")))

    # Aggregate sentiment
    total = {"positive": 0.0, "neutral": 0.0, "negative": 0.0}
    for s in scores:
        for k in total:
            total[k] += s.get(k, 0.0)

    n = len(scores)
    sentiment_avg = {k: round(v / n, 3) for k, v in total.items()}

    return {
        **state,
        "sentiment_score": sentiment_avg
    }