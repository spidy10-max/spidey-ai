"""
Spidey AI — Chat Brain (Updated with Multi-Provider)
Now supports multiple AI providers!
"""
import os
from dotenv import load_dotenv
from spidey.brain.history import ChatHistory
from spidey.brain.providers import ProviderManager

load_dotenv()


class SpideyBrain:
    """Main AI chat class — now with multi-provider support!"""

    def __init__(self, provider="groq"):
        """
        Initialize the AI brain

        Args:
            provider: Which AI provider to use (default: groq)
        """
        # Provider manager handles AI switching
        self.provider_manager = ProviderManager(default_provider=provider)
        self.temperature = 0.7
        self.max_tokens = 1024

        # System prompt — Spidey ki personality
        self.system_prompt = {
            "role": "system",
            "content": (
                "You are Spidey AI, a friendly, witty, and helpful AI assistant. "
                "You are smart, knowledgeable, and always ready to help. "
                "You sometimes use Spider-Man references but keep it professional. "
                "Keep your answers clear, concise, and helpful. "
                "If you don't know something, say so honestly."
            )
        }

        # History manager
        self.history = ChatHistory()

        # Messages list for API calls
        self.messages = [self.system_prompt]

    def start_new_conversation(self):
        """Start a brand new conversation"""
        conv_id = self.history.create_new_conversation()
        self.messages = [self.system_prompt]
        return conv_id

    def chat(self, user_message):
        """
        Send a message to AI and get response

        Args:
            user_message: What the user typed

        Returns:
            AI's response as string
        """
        # Make sure we have a conversation file
        if not self.history.current_file:
            self.start_new_conversation()

        # User ka message add karo
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # Save user message to file
        self.history.add_message("user", user_message)

        # AI se jawab lo (through provider manager)
        result = self.provider_manager.chat(
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        ai_reply = result["content"]

        # AI ka jawab memory mein add karo
        self.messages.append({
            "role": "assistant",
            "content": ai_reply
        })

        # Save AI reply to file
        self.history.add_message("assistant", ai_reply)

        return ai_reply

    def switch_provider(self, provider_name):
        """
        Switch to a different AI provider

        Args:
            provider_name: Provider key (groq, openai, deepseek, etc.)

        Returns:
            True if switched successfully
        """
        return self.provider_manager.switch_provider(provider_name)

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
