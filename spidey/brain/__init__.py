"""
🧠 Spidey Brain Module

Contains:
- chat.py      — Main chat engine (SpideyBrain class)
- providers.py — Multi-AI provider system
- history.py   — Conversation history manager
"""

from spidey.brain.chat import SpideyBrain
from spidey.brain.providers import ProviderManager, AIProvider, PROVIDERS
from spidey.brain.history import ChatHistory

__all__ = [
    "SpideyBrain",
    "ProviderManager",
    "AIProvider",
    "PROVIDERS",
    "ChatHistory"
]
