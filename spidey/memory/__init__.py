"""
🧠 Spidey Memory Module

Contains:
- database.py    — SQLite database manager
- models.py      — Database table schemas
- vector_store.py — ChromaDB vector store
- memory.py      — Memory manager (SQLite + ChromaDB)
- search_engine.py — Smart search engine
- auto_memory.py — Auto-detect user info
"""

from spidey.memory.memory import SpideyMemory
from spidey.memory.database import Database
from spidey.memory.vector_store import VectorStore
from spidey.memory.search_engine import SearchEngine
from spidey.memory.auto_memory import AutoMemory

__all__ = [
    "SpideyMemory",
    "Database",
    "VectorStore",
    "SearchEngine",
    "AutoMemory"
]