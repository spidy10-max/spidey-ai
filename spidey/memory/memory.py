"""
Spidey AI — Memory Manager
Connects the chatbot to SQLite database
Handles saving/retrieving conversations, preferences, and notes
"""
from datetime import datetime
from spidey.memory.database import Database
from spidey.logger import app_logger, log_event, log_error


class SpideyMemory:
    """
    Memory manager for Spidey AI
    
    Handles:
    - Conversation management (create, save, load, delete)
    - User preferences (remember things about user)
    - Personal notes
    - Search across all memory
    """

    def __init__(self):
        """Initialize memory with database connection"""
        self.db = Database()
        self.current_conv_id = None
        app_logger.info("SpideyMemory initialized")

    # ============================================================
    #  CONVERSATION MANAGEMENT
    # ============================================================

    def start_conversation(self, provider="groq", model="llama-3.1-8b-instant"):
        """
        Start a new conversation

        Args:
            provider: AI provider name
            model: AI model name

        Returns:
            Conversation ID string
        """
        conv_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.db.create_conversation(
            conv_id=conv_id,
            provider=provider,
            model=model
        )
        self.current_conv_id = conv_id
        log_event("New conversation started", f"ID: {conv_id}")
        return conv_id

    def save_message(self, role, content, tokens_used=0, provider=None, model=None):
        """
        Save a message to current conversation

        Args:
            role: 'user' or 'assistant'
            content: Message text
            tokens_used: Tokens consumed
            provider: AI provider used
            model: AI model used

        Returns:
            True if saved successfully
        """
        if not self.current_conv_id:
            self.start_conversation()

        success = self.db.add_message(
            conv_id=self.current_conv_id,
            role=role,
            content=content,
            tokens_used=tokens_used,
            provider=provider,
            model=model
        )

        if not success:
            log_error("Failed to save message", "SpideyMemory.save_message")

        return success

    def get_conversation_messages(self, conv_id=None, limit=50):
        """
        Get messages for API calls (role + content only)

        Args:
            conv_id: Conversation ID (default: current)
            limit: Max messages to return

        Returns:
            List of {"role": ..., "content": ...} dicts
        """
        cid = conv_id or self.current_conv_id
        if not cid:
            return []

        return self.db.get_messages_for_api(cid, limit=limit)

    def get_full_messages(self, conv_id=None, limit=100):
        """
        Get full message details (with timestamps, tokens, etc.)

        Args:
            conv_id: Conversation ID (default: current)
            limit: Max messages

        Returns:
            List of full message dicts
        """
        cid = conv_id or self.current_conv_id
        if not cid:
            return []

        return self.db.get_messages(cid, limit=limit)

    def load_conversation(self, conv_id):
        """
        Load a previous conversation

        Args:
            conv_id: Conversation ID to load

        Returns:
            True if loaded successfully
        """
        conv = self.db.get_conversation(conv_id)
        if conv:
            self.current_conv_id = conv_id
            log_event("Conversation loaded", f"ID: {conv_id}")
            return True

        log_error(f"Conversation not found: {conv_id}", "SpideyMemory.load_conversation")
        return False

    def get_all_conversations(self, limit=20):
        """
        Get all conversations list

        Returns:
            List of conversation dicts
        """
        return self.db.get_all_conversations(limit=limit)

    def delete_conversation(self, conv_id):
        """
        Delete a conversation and its messages

        Args:
            conv_id: Conversation ID to delete

        Returns:
            True if deleted
        """
        success = self.db.delete_conversation(conv_id)
        if success and self.current_conv_id == conv_id:
            self.current_conv_id = None
        return success

    def search_conversations(self, query):
        """Search conversations by title"""
        return self.db.search_conversations(query)

    def search_messages(self, query, conv_id=None):
        """
        Search messages across all or specific conversation

        Args:
            query: Search text
            conv_id: Optional specific conversation

        Returns:
            List of matching messages
        """
        return self.db.search_messages(query, conv_id=conv_id)

    def get_message_count(self, conv_id=None):
        """Get message count"""
        return self.db.get_message_count(conv_id or self.current_conv_id)

    # ============================================================
    #  USER PREFERENCES (Remember things about user)
    # ============================================================

    def remember(self, key, value, category="general"):
        """
        Remember something about the user

        Args:
            key: What to remember (e.g., 'name', 'favorite_color')
            value: The value
            category: Category (personal, coding, work, etc.)

        Returns:
            True if saved
        """
        success = self.db.set_preference(key, value, category=category)
        if success:
            log_event("Remembered", f"{key} = {value}")
        return success

    def recall(self, key):
        """
        Recall something about the user

        Args:
            key: What to recall

        Returns:
            Value string or None
        """
        return self.db.get_preference(key)

    def get_all_memories(self):
        """
        Get everything Spidey remembers about user

        Returns:
            Dict of all preferences
        """
        return self.db.get_all_preferences()

    def forget(self, key):
        """
        Forget something about the user

        Args:
            key: What to forget

        Returns:
            True if deleted
        """
        success = self.db.delete_preference(key)
        if success:
            log_event("Forgot", key)
        return success

    def get_memory_context(self):
        """
        Get user memory as context string for AI

        Returns:
            String with all remembered info about user
        """
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
        """
        Add a personal note

        Args:
            title: Note title
            content: Note content
            category: Category
            important: Mark as important

        Returns:
            True if saved
        """
        return self.db.add_note(
            title=title,
            content=content,
            category=category,
            is_important=1 if important else 0
        )

    def get_notes(self, category=None, important_only=False):
        """Get notes with optional filters"""
        return self.db.get_notes(
            category=category,
            important_only=important_only
        )

    def search_notes(self, query):
        """Search notes"""
        return self.db.search_notes(query)

    def delete_note(self, note_id):
        """Delete a note"""
        return self.db.delete_note(note_id)

    # ============================================================
    #  STATISTICS
    # ============================================================

    def get_stats(self):
        """Get memory statistics"""
        return self.db.get_stats()

    # ============================================================
    #  USER MANAGEMENT
    # ============================================================

    def get_user(self):
        """Get current user info"""
        return self.db.get_user(1)

    def update_user(self, username=None, email=None):
        """Update user info"""
        return self.db.update_user(1, username=username, email=email)

    # ============================================================
    #  CLEANUP
    # ============================================================

    def close(self):
        """Close database connection"""
        self.db.close()
