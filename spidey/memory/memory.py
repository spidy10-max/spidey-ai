"""
Spidey AI — Memory Manager (Updated with Vector Store)
Now uses SQLite + ChromaDB together!
"""
from datetime import datetime
from spidey.memory.database import Database
from spidey.memory.vector_store import VectorStore
from spidey.logger import app_logger, log_event, log_error


class SpideyMemory:
    """
    Memory manager for Spidey AI
    SQLite = structured data
    ChromaDB = semantic search
    """

    def __init__(self):
        """Initialize both databases"""
        self.db = Database()
        self.vectors = VectorStore()
        self.current_conv_id = None
        self._message_counter = 0
        app_logger.info("SpideyMemory initialized (SQLite + ChromaDB)")

    # ============================================================
    #  CONVERSATION MANAGEMENT
    # ============================================================

    def start_conversation(self, provider="groq", model="llama-3.1-8b-instant"):
        """Start a new conversation"""
        conv_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.db.create_conversation(
            conv_id=conv_id,
            provider=provider,
            model=model
        )
        self.current_conv_id = conv_id
        self._message_counter = 0
        log_event("New conversation started", f"ID: {conv_id}")
        return conv_id

    def save_message(self, role, content, tokens_used=0, provider=None, model=None):
        """
        Save message to BOTH SQLite and ChromaDB

        SQLite = exact storage
        ChromaDB = semantic search
        """
        if not self.current_conv_id:
            self.start_conversation()

        # Save to SQLite
        success = self.db.add_message(
            conv_id=self.current_conv_id,
            role=role,
            content=content,
            tokens_used=tokens_used,
            provider=provider,
            model=model
        )

        # Save to ChromaDB (for semantic search)
        if success and len(content.strip()) > 5:
            try:
                self._message_counter += 1
                msg_id = f"{self.current_conv_id}_{self._message_counter}"

                self.vectors.add_chat_message(
                    message_id=msg_id,
                    content=content,
                    metadata={
                        "role": role,
                        "conv_id": self.current_conv_id,
                        "provider": provider or "unknown",
                        "timestamp": datetime.now().isoformat()
                    }
                )
            except Exception as e:
                log_error(str(e), "SpideyMemory.save_message (vector)")

        return success

    def get_conversation_messages(self, conv_id=None, limit=50):
        """Get messages for API calls"""
        cid = conv_id or self.current_conv_id
        if not cid:
            return []
        return self.db.get_messages_for_api(cid, limit=limit)

    def get_full_messages(self, conv_id=None, limit=100):
        """Get full message details"""
        cid = conv_id or self.current_conv_id
        if not cid:
            return []
        return self.db.get_messages(cid, limit=limit)

    def load_conversation(self, conv_id):
        """Load a previous conversation"""
        conv = self.db.get_conversation(conv_id)
        if conv:
            self.current_conv_id = conv_id
            log_event("Conversation loaded", f"ID: {conv_id}")
            return True
        return False

    def get_all_conversations(self, limit=20):
        """Get all conversations"""
        return self.db.get_all_conversations(limit=limit)

    def delete_conversation(self, conv_id):
        """Delete a conversation"""
        success = self.db.delete_conversation(conv_id)
        if success and self.current_conv_id == conv_id:
            self.current_conv_id = None
        return success

    def get_message_count(self, conv_id=None):
        """Get message count"""
        return self.db.get_message_count(conv_id or self.current_conv_id)

    # ============================================================
    #  SEMANTIC SEARCH (ChromaDB)
    # ============================================================

    def semantic_search(self, query, n_results=5):
        """
        Search messages by MEANING using ChromaDB

        Args:
            query: What to search for
            n_results: How many results

        Returns:
            List of matching messages
        """
        return self.vectors.search_chats(query, n_results=n_results)

    def search_messages(self, query, conv_id=None):
        """SQL search (exact word match)"""
        return self.db.search_messages(query, conv_id=conv_id)

    def search_conversations(self, query):
        """Search conversations by title"""
        return self.db.search_conversations(query)

    # ============================================================
    #  CONVERSATION SUMMARIES
    # ============================================================

    def save_summary(self, conv_id=None, summary=None):
        """
        Save conversation summary to ChromaDB

        If no summary given, auto-generate from messages
        """
        cid = conv_id or self.current_conv_id
        if not cid:
            return

        if not summary:
            messages = self.db.get_messages(cid, limit=10)
            if messages:
                parts = []
                for msg in messages:
                    if msg["role"] == "user":
                        parts.append(msg["content"][:100])
                summary = "Topics discussed: " + " | ".join(parts[:5])

        if summary:
            conv = self.db.get_conversation(cid)
            self.vectors.add_summary(
                conv_id=cid,
                summary=summary,
                metadata={
                    "title": conv.get("title", "") if conv else "",
                    "timestamp": datetime.now().isoformat()
                }
            )
            log_event("Summary saved", f"Conv: {cid}")

    def search_summaries(self, query, n_results=5):
        """Search conversation summaries by meaning"""
        return self.vectors.search_summaries(query, n_results=n_results)

    # ============================================================
    #  USER PREFERENCES (Remember/Recall)
    # ============================================================

    def remember(self, key, value, category="general"):
        """Remember something — saves to BOTH SQLite and ChromaDB"""
        # Save to SQLite
        success = self.db.set_preference(key, value, category=category)

        # Save to ChromaDB
        if success:
            self.vectors.add_memory(key, value, metadata={
                "category": category,
                "timestamp": datetime.now().isoformat()
            })
            log_event("Remembered", f"{key} = {value}")

        return success

    def recall(self, key):
        """Recall exact memory"""
        return self.db.get_preference(key)

    def get_all_memories(self):
        """Get all memories"""
        return self.db.get_all_preferences()

    def forget(self, key):
        """Forget something — removes from both"""
        success = self.db.delete_preference(key)
        if success:
            self.vectors.delete_memory(key)
            log_event("Forgot", key)
        return success

    def smart_recall(self, query, n_results=3):
        """
        Smart recall — search memories by MEANING

        Example: "what language does user like" → finds "favorite_language: Python"
        """
        return self.vectors.search_memories(query, n_results=n_results)

    def get_memory_context(self):
        """Get user memory as context string for AI"""
        memories = self.get_all_memories()
        if not memories:
            return ""

        lines = ["Here's what I remember about the user:"]
        for key, info in memories.items():
            lines.append(f"- {key}: {info['value']}")

        return "\n".join(lines)

    # ============================================================
    #  NOTES
    # ============================================================

    def add_note(self, title, content, category="general", important=False):
        """Add note to BOTH SQLite and ChromaDB"""
        success = self.db.add_note(
            title=title,
            content=content,
            category=category,
            is_important=1 if important else 0
        )

        if success:
            notes = self.db.get_notes()
            if notes:
                note_id = notes[0]["id"]
                self.vectors.add_note(
                    note_id=note_id,
                    content=f"{title}: {content}",
                    metadata={
                        "category": category,
                        "important": important,
                        "timestamp": datetime.now().isoformat()
                    }
                )

        return success

    def get_notes(self, category=None, important_only=False):
        """Get notes from SQLite"""
        return self.db.get_notes(category=category, important_only=important_only)

    def search_notes(self, query):
        """Search notes by MEANING"""
        return self.vectors.search_notes(query)

    def delete_note(self, note_id):
        """Delete a note"""
        return self.db.delete_note(note_id)

    # ============================================================
    #  STATISTICS
    # ============================================================

    def get_stats(self):
        """Get combined statistics"""
        db_stats = self.db.get_stats()
        vector_stats = self.vectors.get_stats()

        db_stats["vector_messages"] = vector_stats["chat_messages"]
        db_stats["vector_summaries"] = vector_stats["summaries"]
        db_stats["vector_notes"] = vector_stats["notes"]
        db_stats["vector_memories"] = vector_stats["memories"]

        return db_stats

    # ============================================================
    #  USER
    # ============================================================

    def get_user(self):
        return self.db.get_user(1)

    def update_user(self, username=None, email=None):
        return self.db.update_user(1, username=username, email=email)

    # ============================================================
    #  CLEANUP
    # ============================================================

    def close(self):
        """Close connections"""
        self.db.close()