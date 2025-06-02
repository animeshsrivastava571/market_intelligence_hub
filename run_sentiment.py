# run_sentiment.py

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage
from app.core.graph import build_router_graph  # ✅ This is key

graph = build_router_graph()

initial_state = {
    "query": "What's going on with Tesla this week wrt mcp",
    "messages": [HumanMessage(content="What's going on with Tesla this week?")]
}

final_state = graph.invoke(initial_state)
print("📊 Final State:")
print(final_state)
