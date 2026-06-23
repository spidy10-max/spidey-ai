"""
Spidey AI — Chat Brain (Updated with Config System and Logging)
Now uses centralized settings and structured runtime logs.
"""
from spidey.brain.history import ChatHistory
from spidey.brain.providers import ProviderManager
from spidey.config import settings, SYSTEM_PROMPT, CONVERSATIONS_DIR
from spidey.logger import get_logger

logger = get_logger(__name__)


class SpideyBrain:
    """Main AI chat class — now with config system and logging!"""

    def __init__(self):
        """Initialize the AI brain using settings"""
        provider = settings.get("provider", "groq")
        self.temperature = settings.get("temperature", 0.7)
        self.max_tokens = settings.get("max_tokens", 1024)
        self.show_tokens = settings.get("show_tokens", False)

        logger.info("Initializing SpideyBrain with provider=%s temperature=%s max_tokens=%s",
                    provider, self.temperature, self.max_tokens)

        self.provider_manager = ProviderManager(default_provider=provider)

        system_prompt_text = settings.get("system_prompt", SYSTEM_PROMPT)
        self.system_prompt = {
            "role": "system",
            "content": system_prompt_text
        }

        self.history = ChatHistory(history_dir=CONVERSATIONS_DIR)
        self.messages = [self.system_prompt]

    def start_new_conversation(self):
        """Start a brand new conversation"""
        conv_id = self.history.create_new_conversation()
        self.messages = [self.system_prompt]
        logger.info("Started new conversation %s", conv_id)
        return conv_id

    def chat(self, user_message):
        """Send a message to AI and get response"""
        if not self.history.current_file:
            self.start_new_conversation()

        logger.info("User message received: %s", user_message)
        self.messages.append({"role": "user", "content": user_message})
        self.history.add_message("user", user_message)

        result = self.provider_manager.chat(
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        ai_reply = result["content"]
        self.messages.append({"role": "assistant", "content": ai_reply})
        self.history.add_message("assistant", ai_reply)

        logger.info("AI reply saved: provider=%s tokens=%s",
                    result.get("provider"), result.get("total_tokens"))

        if self.show_tokens and result.get("total_tokens", 0) > 0:
            print(f"\n   📊 Tokens: {result['total_tokens']} "
                  f"(in: {result['input_tokens']}, "
                  f"out: {result['output_tokens']})")

        return ai_reply

    def update_settings(self):
        """Reload settings (after user changes them)"""
        self.temperature = settings.get("temperature", 0.7)
        self.max_tokens = settings.get("max_tokens", 1024)
        self.show_tokens = settings.get("show_tokens", False)

        system_prompt_text = settings.get("system_prompt", SYSTEM_PROMPT)
        self.system_prompt = {
            "role": "system",
            "content": system_prompt_text
        }

        logger.info("Updated settings: temperature=%s max_tokens=%s show_tokens=%s",
                    self.temperature, self.max_tokens, self.show_tokens)

    def switch_provider(self, provider_name):
        """Switch to a different AI provider"""
        success = self.provider_manager.switch_provider(provider_name)
        if success:
            settings.set("provider", provider_name)
            logger.info("Provider name changed in settings to %s", provider_name)
        return success

    def get_provider_info(self):
        """Get current provider info"""
        return self.provider_manager.get_current_info()

    def get_provider_name(self):
        """Get current provider name"""
        return self.provider_manager.get_current_name()

    def list_providers(self):
        """List all available providers"""
        return self.provider_manager.list_providers()

    def get_available_providers(self):
        """Get providers with API keys configured"""
        return self.provider_manager.get_available_providers()

    def reset(self):
        """Reset conversation"""
        self.messages = [self.system_prompt]
        self.start_new_conversation()
        logger.info("Conversation reset")

    def load_conversation(self, conv_id):
        """Load a previous conversation"""
        if self.history.load_conversation(conv_id):
            saved_messages = self.history.get_messages()
            self.messages = [self.system_prompt] + saved_messages
            logger.info("Loaded conversation %s with %s messages", conv_id, len(saved_messages))
            return True
        logger.warning("Failed to load conversation %s", conv_id)
        return False

    def get_history_count(self):
        """Kitne messages hue ab tak"""
        return len(self.messages) - 1

    def get_all_conversations(self):
        """Get list of all saved conversations"""
        return self.history.get_all_conversations()

    def delete_conversation(self, conv_id):
        """Delete a conversation"""
        deleted = self.history.delete_conversation(conv_id)
        if deleted:
            logger.info("Deleted conversation %s", conv_id)
        else:
            logger.warning("Could not delete conversation %s", conv_id)
        return deleted
