"""
Spidey AI — Conversation History Manager
Save and load chat history to JSON files
"""
import json
import os
from datetime import datetime


class ChatHistory:
    """Manages saving and loading conversation history"""

    def __init__(self, history_dir="data/conversations"):
        """
        Initialize history manager

        Args:
            history_dir: Folder where conversations are saved
        """
        self.history_dir = history_dir
        self.current_file = None
        self.ensure_directory()

    def ensure_directory(self):
        """Make sure the conversations folder exists"""
        os.makedirs(self.history_dir, exist_ok=True)

    def create_new_conversation(self):
        """
        Start a new conversation file
        Returns the conversation ID
        """
        # Unique ID based on timestamp
        conv_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_file = os.path.join(
            self.history_dir, f"chat_{conv_id}.json"
        )

        # Empty conversation structure
        conversation = {
            "id": conv_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": []
        }

        self._save_json(self.current_file, conversation)
        return conv_id

    def add_message(self, role, content):
        """
        Add a message to current conversation

        Args:
            role: 'user', 'assistant', or 'system'
            content: The message text
        """
        if not self.current_file:
            self.create_new_conversation()

        conversation = self._load_json(self.current_file)

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        conversation["messages"].append(message)
        conversation["updated_at"] = datetime.now().isoformat()

        self._save_json(self.current_file, conversation)

    def get_messages(self):
        """
        Get all messages from current conversation

        Returns:
            List of message dicts [{"role": ..., "content": ...}]
        """
        if not self.current_file or not os.path.exists(self.current_file):
            return []

        conversation = self._load_json(self.current_file)
        # Return only role and content (for API calls)
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in conversation["messages"]
        ]

    def get_all_conversations(self):
        """
        List all saved conversations

        Returns:
            List of conversation summaries
        """
        conversations = []

        if not os.path.exists(self.history_dir):
            return conversations

        for filename in sorted(os.listdir(self.history_dir), reverse=True):
            if filename.endswith(".json"):
                filepath = os.path.join(self.history_dir, filename)
                conv = self._load_json(filepath)

                # Get first user message as preview
                preview = "Empty conversation"
                for msg in conv.get("messages", []):
                    if msg["role"] == "user":
                        preview = msg["content"][:50]
                        break

                conversations.append({
                    "id": conv.get("id", "unknown"),
                    "created_at": conv.get("created_at", ""),
                    "message_count": len(conv.get("messages", [])),
                    "preview": preview,
                    "filepath": filepath
                })

        return conversations

    def load_conversation(self, conv_id):
        """
        Load a specific conversation by ID

        Args:
            conv_id: The conversation ID to load

        Returns:
            True if loaded successfully, False otherwise
        """
        filepath = os.path.join(
            self.history_dir, f"chat_{conv_id}.json"
        )

        if os.path.exists(filepath):
            self.current_file = filepath
            return True
        return False

    def delete_conversation(self, conv_id):
        """
        Delete a conversation by ID

        Args:
            conv_id: The conversation ID to delete

        Returns:
            True if deleted, False if not found
        """
        filepath = os.path.join(
            self.history_dir, f"chat_{conv_id}.json"
        )

        if os.path.exists(filepath):
            os.remove(filepath)
            if self.current_file == filepath:
                self.current_file = None
            return True
        return False

    def get_message_count(self):
        """Get total messages in current conversation"""
        if not self.current_file or not os.path.exists(self.current_file):
            return 0

        conversation = self._load_json(self.current_file)
        return len(conversation.get("messages", []))

    def _save_json(self, filepath, data):
        """Save data to JSON file"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load_json(self, filepath):
        """Load data from JSON file"""
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
