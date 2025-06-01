# app/core/graph.py

from langgraph.graph import StateGraph, END
from app.core.state import AgentState
from app.agents.sentiment_agent import sentiment_agent
from app.agents.news_agent import news_agent
from app.agents.mcp_agent import mcp_agent
from app.agents.router_agent import router_agent
from app.agents.rag_agent import rag_agent
from app.agents.synthesis_agent import synthesis_agent
from app.agents.topic_extraction_agent import topic_extraction_agent


# __all__ = ['build_graph']  # Add this line

def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("topic_extraction", topic_extraction_agent)
    builder.add_node("news", news_agent)
    builder.add_node("sentiment", sentiment_agent)
    builder.add_node("synthesis", synthesis_agent)

    builder.set_entry_point("topic_extraction")
    builder.add_edge("topic_extraction", "news")
    builder.add_edge("news", "sentiment")
    builder.add_edge("sentiment", "synthesis")
    builder.set_finish_point("synthesis")

    return builder.compile()

def build_router_graph():
    builder = StateGraph(AgentState)

    builder.add_node("router", router_agent)
    builder.add_node("news", news_agent)
    builder.add_node("mcp", mcp_agent)
    builder.add_node("rag", rag_agent)
    builder.add_node("sentiment", sentiment_agent)
    builder.add_node("synthesis", synthesis_agent)

    builder.set_entry_point("router")

    builder.add_conditional_edges("router", lambda state: state.get("intent", ""), {
        "news": "news",
        "mcp": "mcp",
        "rag": "rag",
        "sentiment": "sentiment"
    })

    builder.add_edge("news", "synthesis")
    builder.add_edge("mcp", "synthesis")
    builder.add_edge("rag", "synthesis")
    builder.add_edge("sentiment", "synthesis")
    builder.set_finish_point("synthesis")

    return builder.compile()


