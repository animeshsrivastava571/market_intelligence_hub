# app/agents/news_agent.py

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.state import AgentState
from app.tools.news_fetcher import get_recent_news_summaries

def news_agent(state: AgentState) -> AgentState:
    print("🗞️ Running News Agent...")

    topic = state.get("topic", state.get("query", ""))
    summaries = get_recent_news_summaries(topic)

    return {
        **state,
        "news_insights": summaries
    }
