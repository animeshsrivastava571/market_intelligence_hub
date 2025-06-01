import os
import sys
import uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from app.core.graph import build_graph
from app.core.graph import build_router_graph
from app.utils.memory_manager import MemoryManager
from langchain_core.messages import HumanMessage

router = APIRouter()

# 🧠 Global in-memory session store
session_memory_store: Dict[str, MemoryManager] = {}

# ----- Schemas -----

class QueryRequest(BaseModel):
    query: str
    session_id: str

class QueryResponse(BaseModel):
    sentiment_score: dict
    final_summary: str

class SessionResponse(BaseModel):
    session_id: str

class RouterResponse(BaseModel):
    final_summary: str

# ----- Routes -----

@router.get("/start_session", response_model=SessionResponse)
def start_session():
    session_id = str(uuid.uuid4())
    session_memory_store[session_id] = MemoryManager(max_turns=5)
    return {"session_id": session_id}


@router.post("/query", response_model=QueryResponse)
def query_agent(payload: QueryRequest):
    try:
        if payload.session_id not in session_memory_store:
            raise HTTPException(status_code=404, detail="Session not found.")

        memory = session_memory_store[payload.session_id]

        memory.add_human(payload.query)

        graph = build_graph()
        state = graph.invoke({
            "query": payload.query,
            "messages": memory.get()
        })

        memory.add_ai(state.get("final_summary", ""))

        return {
            "sentiment_score": state.get("sentiment_score", {}),
            "final_summary": state.get("final_summary", "No summary generated.")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/route", response_model=QueryResponse)
def route_query_agent(payload: QueryRequest):
    try:
        if payload.session_id not in session_memory_store:
            raise HTTPException(status_code=404, detail="Session not found.")

        memory = session_memory_store[payload.session_id]

        # Add query to memory
        memory.add_human(payload.query)

        # Run the router LangGraph
        graph = build_router_graph()
        state = graph.invoke({
            "query": payload.query,
            "messages": memory.get()
        })

        # Add AI response to memory
        memory.add_ai(state.get("final_summary", ""))

        return {
            "sentiment_score": state.get("sentiment_score", {}),
            "final_summary": state.get("final_summary", "No summary generated.")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))