# app/utils/memory_manager.py

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

class MemoryManager:
    def __init__(self, max_turns=10):
        self.messages: list[BaseMessage] = []
        self.max_turns = max_turns  # Number of total turns (human + AI)

    def add_human(self, text: str):
        if not self.messages or self.messages[-1].content != text:
            self.messages.append(HumanMessage(content=text))
            self._trim()

    def add_ai(self, text: str):
        self.messages.append(AIMessage(content=text))
        self._trim()

    def _trim(self):
        """Ensure memory doesn’t exceed max_turns (each turn = 1 Human + 1 AI)"""
        max_len = self.max_turns * 2  # Human + AI = 2 messages per turn
        if len(self.messages) > max_len:
            self.messages = self.messages[-max_len:]

    def get(self):
        return self.messages
