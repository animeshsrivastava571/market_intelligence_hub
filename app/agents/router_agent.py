# app/agents/router_agent.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.core.state import AgentState
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o")

def router_agent(state: AgentState) -> AgentState:
    query = state["query"]
    messages = state["messages"]

    system_msg = "You are a routing agent that maps a query to one of: news, mcp, rag, sentiment."
    prompt = f"Query: {query}\n\nDecide the most appropriate intent (news/mcp/rag/sentiment). Return ONLY the intent."

    response = llm.invoke([HumanMessage(content=system_msg), HumanMessage(content=prompt)])
    intent = response.content.strip().lower()

    return {
        **state,
        "intent": intent
    }
