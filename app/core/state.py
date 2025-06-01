from typing import TypedDict, List, Optional, Literal, Annotated
from langchain_core.messages import BaseMessage
from operator import add

class AgentState(TypedDict, total=False):
    query: str                                # User query
    messages: Annotated[List[BaseMessage], add]  # Message history for memory
    sentiment_score: Optional[dict]           # FinBERT output
    news_insights: Optional[List[str]]        # RAG-retrieved summaries
    mcp_data: Optional[dict]                  # Financial metrics from SQL
    anomalies: Optional[dict]                 # Detected outliers
    final_summary: Optional[str]              # Output from synthesis agent
