# app/agents/mcp_agent.py

from app.core.state import AgentState
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def mcp_agent(state: AgentState) -> AgentState:
    query = state["query"]

    # Placeholder logic for now
    print(f"🔍 [MCP Agent] Processing query: {query}")
    
    mock_data = {
        "price": "430.21 USD",
        "volatility": "moderate",
        "historical_context": "Last time such a spike occurred, it was due to earnings beat."
    }

    return {
        **state,
        "mcp_result": mock_data
    }