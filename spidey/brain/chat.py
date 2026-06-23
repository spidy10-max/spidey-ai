"""
Spidey AI — Chat Brain (Updated with SQLite Memory)
Now uses database instead of JSON files!
"""
from spidey.brain.providers import ProviderManager
from spidey.memory.memory import SpideyMemory
from spidey.config import settings, SYSTEM_PROMPT
from spidey.logger import brain_logger, log_chat, log_event, log_error


class SpideyBrain:
    """Main AI chat class — now with database memory!"""

    def __init__(self):
        """Initialize the AI brain"""
        # Load settings
        provider = settings.get("provider", "groq")
        self.temperature = settings.get("temperature", 0.7)
        self.max_tokens = settings.get("max_tokens", 1024)
        self.show_tokens = settings.get("show_tokens", False)

        # Provider manager
        self.provider_manager = ProviderManager(default_provider=provider)

        # System prompt
        system_prompt_text = settings.get("system_prompt", SYSTEM_PROMPT)
        self.system_prompt = {
            "role": "system",
            "content": system_prompt_text
        }

        # Memory (SQLite database)
        self.memory = SpideyMemory()

        # Messages list for API calls
        self.messages = [self.system_prompt]

        brain_logger.info("SpideyBrain initialized with SQLite memory")

    def start_new_conversation(self):
        """Start a new conversation"""
        provider_info = self.provider_manager.get_current_info()
        conv_id = self.memory.start_conversation(
            provider=self.provider_manager.get_current_name(),
            model=provider_info.get("model", "unknown")
        )
        self.messages = [self.system_prompt]

        # Add memory context if available
        memory_context = self.memory.get_memory_context()
        if memory_context:
            self.messages.append({
                "role": "system",
                "content": memory_context
            })

        return conv_id

    def chat(self, user_message):
        """
        Send message and get response

        Args:
            user_message: What user typed

        Returns:
            AI response string
        """
        if not self.memory.current_conv_id:
            self.start_new_conversation()

        # Add user message to list
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # Log user message
        log_chat("user", user_message)

        try:
            # Get AI response
            result = self.provider_manager.chat(
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            ai_reply = result["content"]
            provider_name = result.get("provider", "unknown")
            total_tokens = result.get("total_tokens", 0)

            # Add AI reply to messages list
            self.messages.append({
                "role": "assistant",
                "content": ai_reply
            })

            # Save both messages to database
            self.memory.save_message(
                "user", user_message,
                tokens_used=result.get("input_tokens", 0),
                provider=provider_name,
                model=result.get("model")
            )
            self.memory.save_message(
                "assistant", ai_reply,
                tokens_used=result.get("output_tokens", 0),
                provider=provider_name,
                model=result.get("model")
            )

            # Log AI response
            log_chat("assistant", ai_reply, provider=provider_name)

            # Show tokens if enabled
            if self.show_tokens and total_tokens > 0:
                print(f"\n   📊 Tokens: {total_tokens} "
                      f"(in: {result.get('input_tokens', 0)}, "
                      f"out: {result.get('output_tokens', 0)})")

            return ai_reply

        except Exception as e:
            log_error(str(e), "SpideyBrain.chat")
            return f"Error: {str(e)}"

    def update_settings(self):
        """Reload settings"""
        self.temperature = settings.get("temperature", 0.7)
        self.max_tokens = settings.get("max_tokens", 1024)
        self.show_tokens = settings.get("show_tokens", False)

        system_prompt_text = settings.get("system_prompt", SYSTEM_PROMPT)
        self.system_prompt = {
            "role": "system",
            "content": system_prompt_text
        }
        log_event("Settings updated")

    def switch_provider(self, provider_name):
        """Switch AI provider"""
        success = self.provider_manager.switch_provider(provider_name)
        if success:
            settings.set("provider", provider_name)
        return success

    def get_provider_info(self):
        return self.provider_manager.get_current_info()

    def get_provider_name(self):
        return self.provider_manager.get_current_name()

    def list_providers(self):
        return self.provider_manager.list_providers()

    def get_available_providers(self):
        return self.provider_manager.get_available_providers()

    def reset(self):
        """Reset — start fresh conversation"""
        self.start_new_conversation()
        log_event("Conversation reset")

    def load_conversation(self, conv_id):
        """Load a previous conversation"""
        if self.memory.load_conversation(conv_id):
            saved_messages = self.memory.get_conversation_messages(conv_id)
            self.messages = [self.system_prompt]

            # Add memory context
            memory_context = self.memory.get_memory_context()
            if memory_context:
                self.messages.append({
                    "role": "system",
                    "content": memory_context
                })

            self.messages += saved_messages
            return True
        return False

    def get_history_count(self):
        """Message count in current conversation"""
        return self.memory.get_message_count()

    def get_all_conversations(self):
        """Get all conversations"""
        return self.memory.get_all_conversations()

    def delete_conversation(self, conv_id):
        """Delete a conversation"""
        return self.memory.delete_conversation(conv_id)

    def search_chats(self, query):
        """Search across all messages"""
        return self.memory.search_messages(query)

    # ============================================================
    #  MEMORY COMMANDS (Remember/Recall)
    # ============================================================

    def remember(self, key, value, category="general"):
        """Remember something about user"""
        return self.memory.remember(key, value, category)

    def recall(self, key):
        """Recall something about user"""
        return self.memory.recall(key)

    def get_all_memories(self):
        """Get all memories"""
        return self.memory.get_all_memories()

    def forget(self, key):
        """Forget something"""
        return self.memory.forget(key)

    # ============================================================
    #  NOTES
    # ============================================================

    def add_note(self, title, content, category="general", important=False):
        """Add a note"""
        return self.memory.add_note(title, content, category, important)

    def get_notes(self, category=None, important_only=False):
        """Get notes"""
        return self.memory.get_notes(category, important_only)

    def search_notes(self, query):
        """Search notes"""
        return self.memory.search_notes(query)

    def delete_note(self, note_id):
        """Delete a note"""
        return self.memory.delete_note(note_id)

    # ============================================================
    #  STATS
    # ============================================================

    def get_stats(self):
        """Get database stats"""
        return self.memory.get_stats()

    def close(self):
        """Cleanup"""
        self.memory.close()
