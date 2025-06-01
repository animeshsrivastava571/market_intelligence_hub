import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.state import AgentState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def synthesis_agent(state: AgentState) -> AgentState:
    print("🧾 Running Synthesis Agent...")

    sentiment = state.get("sentiment_score", {})
    headlines = state.get("news_insights", [])

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a financial assistant who summarizes news-based sentiment."),
        ("human", """
Here are some recent news headlines:
{headlines}

And here is the sentiment analysis:
Positive: {positive}
Neutral: {neutral}
Negative: {negative}

Summarize what the overall public/media sentiment is toward this topic. Be concise, use natural language, and avoid jargon.
        """)
    ])

    chain = prompt | llm

    output = chain.invoke({
        "headlines": "\n".join(headlines),
        "positive": round(sentiment.get("positive", 0.0), 2),
        "neutral": round(sentiment.get("neutral", 0.0), 2),
        "negative": round(sentiment.get("negative", 0.0), 2),
    })

    # Append assistant response to memory
    messages = state.get("messages", [])
    messages.append(AIMessage(content=output.content))

    return {
        **state,
        "final_summary": output.content,
       # "messages": messages
    }
