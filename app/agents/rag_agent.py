# app/agents/rag_agent.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.state import AgentState

def rag_agent(state: AgentState) -> AgentState:
    query = state["query"]

    # Placeholder RAG behavior
    print(f"📚 [RAG Agent] Retrieving context for query: {query}")

    context = [
        "In March 2023, Nvidia experienced a similar sentiment spike due to AI hype.",
        "Institutional investors showed similar behavior during 2021 earnings cycles."
    ]

    return {
        **state,
        "rag_context": context
    }
