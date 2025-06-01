# app/agents/topic_extraction_agent.py

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.state import AgentState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def topic_extraction_agent(state: AgentState) -> AgentState:
    print("🔎 Running Topic Extraction Agent...")

    query = state.get("query", "")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant that extracts the main financial topic or company from a user's natural query. Respond with only the topic, like 'Tesla' or 'Apple'."),
        ("human", "{query}")
    ])

    chain = prompt | llm
    result = chain.invoke({"query": query})

    return {
        **state,
        "topic": result.content.strip()
    }
