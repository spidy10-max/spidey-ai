"""
Spidey AI — Smart Search Engine
Advanced semantic search across all memory
Combines SQLite (exact) + ChromaDB (meaning) results
"""
from spidey.memory.database import Database
from spidey.memory.vector_store import VectorStore
from spidey.config import DATA_DIR, CONVERSATIONS_DIR
from spidey.logger import app_logger, log_event, log_error
import os


class SearchEngine:
    """
    Smart search engine for Spidey AI

    Combines:
    - SQLite exact word search
    - ChromaDB semantic (meaning) search
    - Ranked results by relevance
    """

    def __init__(self, db=None, vectors=None):
        """
        Initialize search engine

        Args:
            db: Existing Database instance
            vectors: Existing VectorStore instance
        """
        self.db = db or Database()
        self.vectors = vectors or VectorStore()
        app_logger.info("SearchEngine initialized")

    def smart_search(self, query, n_results=10):
        """
        Combined search — both exact AND semantic

        Args:
            query: What to search for
            n_results: Max results

        Returns:
            Dict with categorized results
        """
        results = {
            "query": query,
            "semantic_messages": [],
            "exact_messages": [],
            "summaries": [],
            "memories": [],
            "notes": [],
            "total_found": 0
        }

        # 1. Semantic search (by meaning)
        try:
            semantic = self.vectors.search_chats(query, n_results=n_results)
            results["semantic_messages"] = semantic
        except Exception as e:
            log_error(str(e), "SearchEngine.smart_search (semantic)")

        # 2. Exact search (by words)
        try:
            exact = self.db.search_messages(query)
            results["exact_messages"] = exact[:n_results]
        except Exception as e:
            log_error(str(e), "SearchEngine.smart_search (exact)")

        # 3. Summary search
        try:
            summaries = self.vectors.search_summaries(query, n_results=5)
            results["summaries"] = summaries
        except Exception as e:
            log_error(str(e), "SearchEngine.smart_search (summaries)")

        # 4. Memory search
        try:
            memories = self.vectors.search_memories(query, n_results=5)
            results["memories"] = memories
        except Exception as e:
            log_error(str(e), "SearchEngine.smart_search (memories)")

        # 5. Note search
        try:
            notes = self.vectors.search_notes(query, n_results=5)
            results["notes"] = notes
        except Exception as e:
            log_error(str(e), "SearchEngine.smart_search (notes)")

        # Count total
        results["total_found"] = (
            len(results["semantic_messages"]) +
            len(results["exact_messages"]) +
            len(results["summaries"]) +
            len(results["memories"]) +
            len(results["notes"])
        )

        log_event("Smart search", f"Query: '{query}' → {results['total_found']} results")
        return results

    def find_related_chats(self, message, n_results=5):
        """
        Find chats related to a specific message

        Args:
            message: The message to find related chats for
            n_results: How many results

        Returns:
            List of related messages
        """
        try:
            results = self.vectors.search_chats(message, n_results=n_results)
            return results
        except Exception as e:
            log_error(str(e), "SearchEngine.find_related_chats")
            return []

    def find_conversations_about(self, topic, n_results=5):
        """
        Find conversations about a specific topic

        Args:
            topic: What topic to search
            n_results: How many results

        Returns:
            List of matching conversation summaries
        """
        try:
            # Search summaries first
            summaries = self.vectors.search_summaries(topic, n_results=n_results)

            # Also search messages and group by conversation
            messages = self.vectors.search_chats(topic, n_results=n_results * 2)

            # Get unique conversation IDs from messages
            conv_ids = set()
            for msg in messages:
                conv_id = msg.get("metadata", {}).get("conv_id")
                if conv_id:
                    conv_ids.add(conv_id)

            # Get conversation details
            conversations = []
            for conv_id in conv_ids:
                conv = self.db.get_conversation(conv_id)
                if conv:
                    # Count relevant messages in this conversation
                    relevant_count = sum(
                        1 for m in messages
                        if m.get("metadata", {}).get("conv_id") == conv_id
                    )
                    conv["relevant_messages"] = relevant_count
                    conversations.append(conv)

            # Sort by relevance
            conversations.sort(key=lambda x: x.get("relevant_messages", 0), reverse=True)

            return {
                "summaries": summaries,
                "conversations": conversations[:n_results]
            }

        except Exception as e:
            log_error(str(e), "SearchEngine.find_conversations_about")
            return {"summaries": [], "conversations": []}

    def get_context_for_query(self, query, n_results=3):
        """
        Get relevant context from past chats for AI

        This helps AI give better answers by knowing past conversations

        Args:
            query: User's current message
            n_results: How many past messages to include

        Returns:
            Context string to add to AI prompt
        """
        try:
            # Search for relevant past messages
            relevant = self.vectors.search_chats(query, n_results=n_results)

            # Search for relevant memories
            memories = self.vectors.search_memories(query, n_results=2)

            if not relevant and not memories:
                return ""

            context_parts = []

            if relevant:
                context_parts.append("Relevant past conversations:")
                for r in relevant:
                    role = r.get("metadata", {}).get("role", "unknown")
                    content = r["content"][:150]
                    context_parts.append(f"- [{role}]: {content}")

            if memories:
                context_parts.append("\nRelevant user info:")
                for m in memories:
                    context_parts.append(f"- {m['content']}")

            return "\n".join(context_parts)

        except Exception as e:
            log_error(str(e), "SearchEngine.get_context_for_query")
            return ""

    def search_by_date(self, date_str):
        """
        Search conversations by date

        Args:
            date_str: Date string (e.g., "2026-06-23")

        Returns:
            List of conversations from that date
        """
        try:
            all_convs = self.db.get_all_conversations(limit=100)
            matching = [
                conv for conv in all_convs
                if conv.get("created_at", "").startswith(date_str)
            ]
            return matching
        except Exception as e:
            log_error(str(e), "SearchEngine.search_by_date")
            return []

    def get_search_stats(self):
        """Get search-related statistics"""
        vector_stats = self.vectors.get_stats()
        db_stats = self.db.get_stats()

        return {
            "total_searchable_messages": vector_stats["chat_messages"],
            "total_summaries": vector_stats["summaries"],
            "total_memories": vector_stats["memories"],
            "total_notes": vector_stats["notes"],
            "total_db_messages": db_stats["total_messages"],
            "total_conversations": db_stats["total_conversations"]
        }