"""
Spidey AI — SQLite Database Manager
Handles all database operations: create, read, update, delete
"""
import sqlite3
import os
from datetime import datetime
from spidey.memory.models import ALL_TABLES
from spidey.config import DATA_DIR
from spidey.logger import app_logger, log_event, log_error


# Database file path
DB_PATH = os.path.join(DATA_DIR, "spidey.db")


class Database:
    """
    SQLite Database Manager for Spidey AI

    Handles:
    - Database creation and initialization
    - CRUD operations for all tables
    - Connection management
    """

    def __init__(self, db_path=None):
        """
        Initialize database connection

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path or DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.connection = None
        self.connect()
        self.initialize_tables()

    def connect(self):
        """Create database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            # Return rows as dictionaries
            self.connection.row_factory = sqlite3.Row
            # Enable foreign keys
            self.connection.execute("PRAGMA foreign_keys = ON")
            app_logger.info(f"Database connected: {self.db_path}")
        except sqlite3.Error as e:
            log_error(str(e), "Database.connect")
            raise

    def initialize_tables(self):
        """Create all tables if they don't exist"""
        try:
            cursor = self.connection.cursor()
            for table_name, create_sql in ALL_TABLES:
                cursor.execute(create_sql)
                app_logger.debug(f"Table ready: {table_name}")

            # Create default user if not exists
            cursor.execute(
                "SELECT COUNT(*) FROM users"
            )
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO users (username) VALUES (?)",
                    ("User",)
                )
                app_logger.info("Default user created")

            self.connection.commit()
            log_event("Database initialized", f"Tables: {len(ALL_TABLES)}")

        except sqlite3.Error as e:
            log_error(str(e), "Database.initialize_tables")
            raise

    # ============================================================
    #  USER OPERATIONS
    # ============================================================

    def get_user(self, user_id=1):
        """Get user by ID"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_user(self, user_id=1, username=None, email=None):
        """Update user info"""
        try:
            updates = []
            values = []

            if username:
                updates.append("username = ?")
                values.append(username)
            if email:
                updates.append("email = ?")
                values.append(email)

            if not updates:
                return False

            updates.append("updated_at = ?")
            values.append(datetime.now().isoformat())
            values.append(user_id)

            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            self.connection.execute(query, values)
            self.connection.commit()
            return True

        except sqlite3.Error as e:
            log_error(str(e), "Database.update_user")
            return False

    # ============================================================
    #  CONVERSATION OPERATIONS
    # ============================================================

    def create_conversation(self, conv_id, title=None, provider="groq", model="llama-3.1-8b-instant"):
        """Create a new conversation"""
        try:
            if title is None:
                title = f"Chat {datetime.now().strftime('%b %d, %H:%M')}"

            self.connection.execute(
                """INSERT INTO conversations (conv_id, title, provider, model)
                   VALUES (?, ?, ?, ?)""",
                (conv_id, title, provider, model)
            )
            self.connection.commit()
            app_logger.debug(f"Conversation created: {conv_id}")
            return conv_id

        except sqlite3.Error as e:
            log_error(str(e), "Database.create_conversation")
            return None

    def get_conversation(self, conv_id):
        """Get a specific conversation"""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM conversations WHERE conv_id = ?",
            (conv_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_conversations(self, limit=20, include_archived=False):
        """Get all conversations sorted by latest"""
        cursor = self.connection.cursor()

        if include_archived:
            cursor.execute(
                """SELECT * FROM conversations
                   ORDER BY updated_at DESC LIMIT ?""",
                (limit,)
            )
        else:
            cursor.execute(
                """SELECT * FROM conversations
                   WHERE is_archived = 0
                   ORDER BY updated_at DESC LIMIT ?""",
                (limit,)
            )

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def update_conversation(self, conv_id, title=None):
        """Update conversation title"""
        try:
            if title:
                self.connection.execute(
                    """UPDATE conversations
                       SET title = ?, updated_at = ?
                       WHERE conv_id = ?""",
                    (title, datetime.now().isoformat(), conv_id)
                )
                self.connection.commit()
            return True
        except sqlite3.Error as e:
            log_error(str(e), "Database.update_conversation")
            return False

    def archive_conversation(self, conv_id):
        """Archive a conversation (soft delete)"""
        try:
            self.connection.execute(
                """UPDATE conversations SET is_archived = 1
                   WHERE conv_id = ?""",
                (conv_id,)
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            log_error(str(e), "Database.archive_conversation")
            return False

    def delete_conversation(self, conv_id):
        """Delete conversation and its messages"""
        try:
            self.connection.execute(
                "DELETE FROM messages WHERE conv_id = ?",
                (conv_id,)
            )
            self.connection.execute(
                "DELETE FROM conversations WHERE conv_id = ?",
                (conv_id,)
            )
            self.connection.commit()
            log_event("Conversation deleted", f"ID: {conv_id}")
            return True
        except sqlite3.Error as e:
            log_error(str(e), "Database.delete_conversation")
            return False

    def search_conversations(self, query):
        """Search conversations by title"""
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT * FROM conversations
               WHERE title LIKE ?
               ORDER BY updated_at DESC""",
            (f"%{query}%",)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    # ============================================================
    #  MESSAGE OPERATIONS
    # ============================================================

    def add_message(self, conv_id, role, content, tokens_used=0, provider=None, model=None):
        """Add a message to a conversation"""
        try:
            self.connection.execute(
                """INSERT INTO messages (conv_id, role, content, tokens_used, provider, model)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (conv_id, role, content, tokens_used, provider, model)
            )

            # Update conversation message count and timestamp
            self.connection.execute(
                """UPDATE conversations
                   SET message_count = message_count + 1,
                       updated_at = ?
                   WHERE conv_id = ?""",
                (datetime.now().isoformat(), conv_id)
            )

            # Auto-set title from first user message
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT message_count FROM conversations WHERE conv_id = ?",
                (conv_id,)
            )
            row = cursor.fetchone()
            if row and row[0] == 1 and role == "user":
                title = content[:50]
                self.update_conversation(conv_id, title=title)

            self.connection.commit()
            return True

        except sqlite3.Error as e:
            log_error(str(e), "Database.add_message")
            return False

    def get_messages(self, conv_id, limit=100):
        """Get all messages for a conversation"""
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT * FROM messages
               WHERE conv_id = ?
               ORDER BY created_at ASC
               LIMIT ?""",
            (conv_id, limit)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_messages_for_api(self, conv_id, limit=50):
        """Get messages formatted for AI API calls"""
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT role, content FROM messages
               WHERE conv_id = ?
               ORDER BY created_at ASC
               LIMIT ?""",
            (conv_id, limit)
        )
        rows = cursor.fetchall()
        return [{"role": row[0], "content": row[1]} for row in rows]

    def search_messages(self, query, conv_id=None):
        """Search messages by content"""
        cursor = self.connection.cursor()

        if conv_id:
            cursor.execute(
                """SELECT m.*, c.title as conv_title
                   FROM messages m
                   JOIN conversations c ON m.conv_id = c.conv_id
                   WHERE m.content LIKE ? AND m.conv_id = ?
                   ORDER BY m.created_at DESC""",
                (f"%{query}%", conv_id)
            )
        else:
            cursor.execute(
                """SELECT m.*, c.title as conv_title
                   FROM messages m
                   JOIN conversations c ON m.conv_id = c.conv_id
                   WHERE m.content LIKE ?
                   ORDER BY m.created_at DESC
                   LIMIT 20""",
                (f"%{query}%",)
            )

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_message_count(self, conv_id=None):
        """Get total message count"""
        cursor = self.connection.cursor()
        if conv_id:
            cursor.execute(
                "SELECT COUNT(*) FROM messages WHERE conv_id = ?",
                (conv_id,)
            )
        else:
            cursor.execute("SELECT COUNT(*) FROM messages")
        return cursor.fetchone()[0]

    # ============================================================
    #  PREFERENCES OPERATIONS
    # ============================================================

    def set_preference(self, key, value, category="general", user_id=1):
        """Set a user preference (insert or update)"""
        try:
            self.connection.execute(
                """INSERT INTO user_preferences (user_id, key, value, category, updated_at)
                   VALUES (?, ?, ?, ?, ?)
                   ON CONFLICT(user_id, key)
                   DO UPDATE SET value = ?, category = ?, updated_at = ?""",
                (user_id, key, value, category, datetime.now().isoformat(),
                 value, category, datetime.now().isoformat())
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            log_error(str(e), "Database.set_preference")
            return False

    def get_preference(self, key, user_id=1):
        """Get a specific preference"""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT value FROM user_preferences WHERE key = ? AND user_id = ?",
            (key, user_id)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def get_all_preferences(self, user_id=1):
        """Get all preferences for a user"""
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT key, value, category FROM user_preferences
               WHERE user_id = ?
               ORDER BY category, key""",
            (user_id,)
        )
        rows = cursor.fetchall()
        return {row[0]: {"value": row[1], "category": row[2]} for row in rows}

    def delete_preference(self, key, user_id=1):
        """Delete a preference"""
        try:
            self.connection.execute(
                "DELETE FROM user_preferences WHERE key = ? AND user_id = ?",
                (key, user_id)
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            log_error(str(e), "Database.delete_preference")
            return False

    # ============================================================
    #  NOTES OPERATIONS
    # ============================================================

    def add_note(self, title, content, category="general", is_important=0):
        """Add a personal note"""
        try:
            self.connection.execute(
                """INSERT INTO notes (title, content, category, is_important)
                   VALUES (?, ?, ?, ?)""",
                (title, content, category, is_important)
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            log_error(str(e), "Database.add_note")
            return False

    def get_notes(self, category=None, important_only=False):
        """Get notes with optional filters"""
        cursor = self.connection.cursor()

        if important_only:
            cursor.execute(
                "SELECT * FROM notes WHERE is_important = 1 ORDER BY created_at DESC"
            )
        elif category:
            cursor.execute(
                "SELECT * FROM notes WHERE category = ? ORDER BY created_at DESC",
                (category,)
            )
        else:
            cursor.execute(
                "SELECT * FROM notes ORDER BY created_at DESC"
            )

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def search_notes(self, query):
        """Search notes by title or content"""
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT * FROM notes
               WHERE title LIKE ? OR content LIKE ?
               ORDER BY created_at DESC""",
            (f"%{query}%", f"%{query}%")
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def delete_note(self, note_id):
        """Delete a note by ID"""
        try:
            self.connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            log_error(str(e), "Database.delete_note")
            return False

    # ============================================================
    #  STATISTICS
    # ============================================================

    def get_stats(self):
        """Get database statistics"""
        cursor = self.connection.cursor()

        stats = {}

        cursor.execute("SELECT COUNT(*) FROM conversations WHERE is_archived = 0")
        stats["total_conversations"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM messages")
        stats["total_messages"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM messages WHERE role = 'user'")
        stats["user_messages"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM messages WHERE role = 'assistant'")
        stats["ai_messages"] = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(tokens_used) FROM messages")
        result = cursor.fetchone()[0]
        stats["total_tokens"] = result if result else 0

        cursor.execute("SELECT COUNT(*) FROM notes")
        stats["total_notes"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM user_preferences")
        stats["total_preferences"] = cursor.fetchone()[0]

        return stats

    # ============================================================
    #  CLEANUP

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            app_logger.info("Database connection closed")

    def __del__(self):
        """Cleanup on deletion"""
        self.close()
