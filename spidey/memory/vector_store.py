"""
Spidey AI — Vector Store (ChromaDB)
Semantic search using vector embeddings
"""
import chromadb
import os
from datetime import datetime
from spidey.config import DATA_DIR
from spidey.logger import app_logger, log_event, log_error


CHROMA_DIR = os.path.join(DATA_DIR, "chroma")


class VectorStore:
    """Vector database for semantic search"""

    def __init__(self, persist_dir=None):
        self.persist_dir = persist_dir or CHROMA_DIR
        os.makedirs(self.persist_dir, exist_ok=True)

        try:
            self.client = chromadb.PersistentClient(path=self.persist_dir)
            app_logger.info(f"ChromaDB initialized: {self.persist_dir}")
        except Exception as e:
            log_error(str(e), "VectorStore.__init__")
            raise

        self._init_collections()

    def _init_collections(self):
        """Create or get all collections"""
        try:
            self.chat_collection = self.client.get_or_create_collection(
                name="chat_messages",
                metadata={"description": "All chat messages for semantic search"}
            )
            self.summary_collection = self.client.get_or_create_collection(
                name="conversation_summaries",
                metadata={"description": "Summaries of conversations"}
            )
            self.notes_collection = self.client.get_or_create_collection(
                name="user_notes",
                metadata={"description": "User personal notes"}
            )
            self.memory_collection = self.client.get_or_create_collection(
                name="user_memories",
                metadata={"description": "Facts about the user"}
            )
            app_logger.info("ChromaDB collections ready")
        except Exception as e:
            log_error(str(e), "VectorStore._init_collections")
            raise

    # ============================================================
    #  CHAT MESSAGES
    # ============================================================

    def add_chat_message(self, message_id, content, metadata=None):
        """Add a chat message to vector store"""
        try:
            if metadata is None:
                metadata = {}
            metadata["added_at"] = datetime.now().isoformat()
            self.chat_collection.add(
                ids=[str(message_id)],
                documents=[content],
                metadatas=[metadata]
            )
        except Exception as e:
            log_error(str(e), "VectorStore.add_chat_message")

    def search_chats(self, query, n_results=5, filter_metadata=None):
        """Search chat messages by meaning"""
        try:
            if self.chat_collection.count() == 0:
                return []

            kwargs = {
                "query_texts": [query],
                "n_results": min(n_results, self.chat_collection.count())
            }
            if filter_metadata:
                kwargs["where"] = filter_metadata

            results = self.chat_collection.query(**kwargs)

            formatted = []
            if results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted.append({
                        "content": doc,
                        "id": results["ids"][0][i] if results["ids"] else None,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0
                    })
            return formatted
        except Exception as e:
            log_error(str(e), "VectorStore.search_chats")
            return []

    # ============================================================
    #  CONVERSATION SUMMARIES
    # ============================================================

    def add_summary(self, conv_id, summary, metadata=None):
        """Add a conversation summary"""
        try:
            if metadata is None:
                metadata = {}
            metadata["added_at"] = datetime.now().isoformat()
            self.summary_collection.upsert(
                ids=[str(conv_id)],
                documents=[summary],
                metadatas=[metadata]
            )
        except Exception as e:
            log_error(str(e), "VectorStore.add_summary")

    def search_summaries(self, query, n_results=5):
        """Search conversation summaries by meaning"""
        try:
            if self.summary_collection.count() == 0:
                return []
            results = self.summary_collection.query(
                query_texts=[query],
                n_results=min(n_results, self.summary_collection.count())
            )
            formatted = []
            if results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted.append({
                        "content": doc,
                        "conv_id": results["ids"][0][i] if results["ids"] else None,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0
                    })
            return formatted
        except Exception as e:
            log_error(str(e), "VectorStore.search_summaries")
            return []

    # ============================================================
    #  NOTES
    # ============================================================

    def add_note(self, note_id, content, metadata=None):
        """Add a note to vector store"""
        try:
            if metadata is None:
                metadata = {}
            metadata["added_at"] = datetime.now().isoformat()
            self.notes_collection.upsert(
                ids=[str(note_id)],
                documents=[content],
                metadatas=[metadata]
            )
        except Exception as e:
            log_error(str(e), "VectorStore.add_note")

    def search_notes(self, query, n_results=5):
        """Search notes by meaning"""
        try:
            if self.notes_collection.count() == 0:
                return []
            results = self.notes_collection.query(
                query_texts=[query],
                n_results=min(n_results, self.notes_collection.count())
            )
            formatted = []
            if results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted.append({
                        "content": doc,
                        "id": results["ids"][0][i] if results["ids"] else None,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0
                    })
            return formatted
        except Exception as e:
            log_error(str(e), "VectorStore.search_notes")
            return []

    # ============================================================
    #  USER MEMORIES
    # ============================================================

    def add_memory(self, key, value, metadata=None):
        """Add a user memory/fact"""
        try:
            if metadata is None:
                metadata = {}
            metadata["key"] = key
            metadata["added_at"] = datetime.now().isoformat()
            self.memory_collection.upsert(
                ids=[str(key)],
                documents=[f"{key}: {value}"],
                metadatas=[metadata]
            )
        except Exception as e:
            log_error(str(e), "VectorStore.add_memory")

    def search_memories(self, query, n_results=5):
        """Search user memories by meaning"""
        try:
            if self.memory_collection.count() == 0:
                return []
            results = self.memory_collection.query(
                query_texts=[query],
                n_results=min(n_results, self.memory_collection.count())
            )
            formatted = []
            if results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted.append({
                        "content": doc,
                        "id": results["ids"][0][i] if results["ids"] else None,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0
                    })
            return formatted
        except Exception as e:
            log_error(str(e), "VectorStore.search_memories")
            return []

    def delete_memory(self, key):
        """Delete a memory from vector store"""
        try:
            self.memory_collection.delete(ids=[str(key)])
        except Exception as e:
            log_error(str(e), "VectorStore.delete_memory")

    # ============================================================
    #  UTILITIES
    # ============================================================

    def get_stats(self):
        """Get vector store statistics"""
        return {
            "chat_messages": self.chat_collection.count(),
            "summaries": self.summary_collection.count(),
            "notes": self.notes_collection.count(),
            "memories": self.memory_collection.count()
        }

    def delete_collection(self, name):
        """Delete an entire collection"""
        try:
            self.client.delete_collection(name)
            self._init_collections()
            log_event(f"Collection deleted: {name}")
        except Exception as e:
            log_error(str(e), "VectorStore.delete_collection")