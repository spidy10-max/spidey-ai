"""
Spidey AI — Chat Brain (Updated with Semantic Memory)
Now saves to SQLite + ChromaDB!
"""
from spidey.brain.providers import ProviderManager
from spidey.memory.memory import SpideyMemory
from spidey.config import settings, SYSTEM_PROMPT
from spidey.logger import brain_logger, log_chat, log_event, log_error


class SpideyBrain:
    """Main AI chat class — with full memory!"""

    def __init__(self):
        """Initialize the AI brain"""
        provider = settings.get("provider", "groq")
        self.temperature = settings.get("temperature", 0.7)
        self.max_tokens = settings.get("max_tokens", 1024)
        self.show_tokens = settings.get("show_tokens", False)

        self.provider_manager = ProviderManager(default_provider=provider)

        system_prompt_text = settings.get("system_prompt", SYSTEM_PROMPT)
        self.system_prompt = {
            "role": "system",
            "content": system_prompt_text
        }

        # Memory (SQLite + ChromaDB)
        self.memory = SpideyMemory()
        self.messages = [self.system_prompt]

        brain_logger.info("SpideyBrain initialized with full memory")

    def start_new_conversation(self):
        """Start new conversation"""
        provider_info = self.provider_manager.get_current_info()
        conv_id = self.memory.start_conversation(
            provider=self.provider_manager.get_current_name(),
            model=provider_info.get("model", "unknown")
        )
        self.messages = [self.system_prompt]

        memory_context = self.memory.get_memory_context()
        if memory_context:
            self.messages.append({
                "role": "system",
                "content": memory_context
            })

        return conv_id

    def chat(self, user_message):
        """Send message and get response"""
        if not self.memory.current_conv_id:
            self.start_new_conversation()

        self.messages.append({
            "role": "user",
            "content": user_message
        })

        log_chat("user", user_message)

        try:
            result = self.provider_manager.chat(
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            ai_reply = result["content"]
            provider_name = result.get("provider", "unknown")
            total_tokens = result.get("total_tokens", 0)

            self.messages.append({
                "role": "assistant",
                "content": ai_reply
            })

            # Save to SQLite + ChromaDB
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

            log_chat("assistant", ai_reply, provider=provider_name)

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
        self.system_prompt = {"role": "system", "content": system_prompt_text}
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
        """Reset conversation + save summary"""
        if self.memory.current_conv_id:
            self.memory.save_summary()
        self.start_new_conversation()
        log_event("Conversation reset")

    def load_conversation(self, conv_id):
        """Load previous conversation"""
        if self.memory.load_conversation(conv_id):
            saved_messages = self.memory.get_conversation_messages(conv_id)
            self.messages = [self.system_prompt]
            memory_context = self.memory.get_memory_context()
            if memory_context:
                self.messages.append({"role": "system", "content": memory_context})
            self.messages += saved_messages
            return True
        return False

    def get_history_count(self):
        return self.memory.get_message_count()

    def get_all_conversations(self):
        return self.memory.get_all_conversations()

    def delete_conversation(self, conv_id):
        return self.memory.delete_conversation(conv_id)

    # === SEARCH ===
    def semantic_search(self, query, n_results=5):
        """Search by MEANING"""
        return self.memory.semantic_search(query, n_results)

    def search_chats(self, query):
        """Search by exact words"""
        return self.memory.search_messages(query)

    def search_summaries(self, query):
        """Search conversation summaries"""
        return self.memory.search_summaries(query)

    # === MEMORY ===
    def remember(self, key, value, category="general"):
        return self.memory.remember(key, value, category)

    def recall(self, key):
        return self.memory.recall(key)

    def smart_recall(self, query):
        """Search memories by meaning"""
        return self.memory.smart_recall(query)

    def get_all_memories(self):
        return self.memory.get_all_memories()

    def forget(self, key):
        return self.memory.forget(key)

    # === NOTES ===
    def add_note(self, title, content, category="general", important=False):
        return self.memory.add_note(title, content, category, important)

    def get_notes(self, category=None, important_only=False):
        return self.memory.get_notes(category, important_only)

    def search_notes(self, query):
        return self.memory.search_notes(query)

    def delete_note(self, note_id):
        return self.memory.delete_note(note_id)

    # === STATS ===
    def get_stats(self):
        return self.memory.get_stats()

    def close(self):
        """Save summary and cleanup"""
        if self.memory.current_conv_id:
            self.memory.save_summary()
        self.memory.close()