"""
Spidey AI — Chat Brain (Updated with Config System)
Now uses centralized settings!
"""
from spidey.brain.history import ChatHistory
from spidey.brain.providers import ProviderManager
from spidey.config import settings, SYSTEM_PROMPT, CONVERSATIONS_DIR


class SpideyBrain:
    """Main AI chat class — now with config system!"""

    def __init__(self):
        """Initialize the AI brain using settings"""
        # Load settings
        provider = settings.get("provider", "groq")
        self.temperature = settings.get("temperature", 0.7)
        self.max_tokens = settings.get("max_tokens", 1024)
        self.show_tokens = settings.get("show_tokens", False)

        # Provider manager
        self.provider_manager = ProviderManager(default_provider=provider)

        # System prompt from settings
        system_prompt_text = settings.get("system_prompt", SYSTEM_PROMPT)
        self.system_prompt = {
            "role": "system",
            "content": system_prompt_text
        }

        # History manager
        self.history = ChatHistory(history_dir=CONVERSATIONS_DIR)

        # Messages list
        self.messages = [self.system_prompt]

    def start_new_conversation(self):
        """Start a brand new conversation"""
        conv_id = self.history.create_new_conversation()
        self.messages = [self.system_prompt]
        return conv_id

    def chat(self, user_message):
        """Send a message to AI and get response"""
        if not self.history.current_file:
            self.start_new_conversation()

        self.messages.append({
            "role": "user",
            "content": user_message
        })

        self.history.add_message("user", user_message)

        result = self.provider_manager.chat(
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        ai_reply = result["content"]

        self.messages.append({
            "role": "assistant",
            "content": ai_reply
        })

        self.history.add_message("assistant", ai_reply)

        # Show token usage if enabled
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

        # Update system prompt if changed
        system_prompt_text = settings.get("system_prompt", SYSTEM_PROMPT)
        self.system_prompt = {
            "role": "system",
            "content": system_prompt_text
        }

    def switch_provider(self, provider_name):
        """Switch to a different AI provider"""
        success = self.provider_manager.switch_provider(provider_name)
        if success:
            settings.set("provider", provider_name)
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

    def load_conversation(self, conv_id):
        """Load a previous conversation"""
        if self.history.load_conversation(conv_id):
            saved_messages = self.history.get_messages()
            self.messages = [self.system_prompt] + saved_messages
            return True
        return False

    def get_history_count(self):
        """Kitne messages hue ab tak"""
        return len(self.messages) - 1

    def get_all_conversations(self):
        """Get list of all saved conversations"""
        return self.history.get_all_conversations()

    def delete_conversation(self, conv_id):
        """Delete a conversation"""
        return self.history.delete_conversation(conv_id)
