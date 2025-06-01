# run_sentiment.py

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from app.core.graph import build_graph
from app.utils.memory_manager import MemoryManager

load_dotenv()

graph = build_graph()
memory = MemoryManager(max_turns=5)

# Turn 1
query_1 = "What's going on with Tesla this week?"
memory.add_human(query_1)

state_1 = graph.invoke({
    "query": query_1,
    "messages": memory.get()
})

memory.add_ai(state_1["final_summary"])

# Turn 2
query_2 = "And what about Nvidia?"
memory.add_human(query_2)

state_2 = graph.invoke({
    "query": query_2,
    "messages": memory.get()
})

memory.add_ai(state_2["final_summary"])

# Print Final State
print("\n🟢 Final Summary (Tesla):", state_1["final_summary"])
print("\n🟣 Final Summary (Nvidia):", state_2["final_summary"])

print("\n🧠 Memory:")
for msg in memory.get():
    print(f"{msg.type.upper()}: {msg.content}")
