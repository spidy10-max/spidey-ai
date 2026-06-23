"""
Spidey AI — Chat Brain (Updated with History Saving)
Now saves all conversations to JSON files!
"""
import openai
import os
from dotenv import load_dotenv
from spidey.brain.history import ChatHistory

load_dotenv()


class SpideyBrain:
    """Main AI chat class for Spidey — now with persistent memory!"""

    def __init__(self):
        """Initialize the AI brain with Groq API and history"""
        self.client = openai.OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = "llama-3.1-8b-instant"
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
        Now also saves to JSON file!

        Args:
            user_message: What the user typed

        Returns:
            AI's response as string
        """
        # Make sure we have a conversation file
        if not self.history.current_file:
            self.start_new_conversation()

        # User ka message history mein add karo
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # Save user message to file
        self.history.add_message("user", user_message)

        try:
            # AI ko message bhejo
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            # AI ka jawab nikalo
            ai_reply = response.choices[0].message.content

            # AI ka jawab memory mein add karo
            self.messages.append({
                "role": "assistant",
                "content": ai_reply
            })

            # Save AI reply to file
            self.history.add_message("assistant", ai_reply)

            return ai_reply

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            return error_msg

    def reset(self):
        """Reset conversation — naye siray se shuru karo"""
        self.messages = [self.system_prompt]
        self.start_new_conversation()

    def load_conversation(self, conv_id):
        """
        Load a previous conversation

        Args:
            conv_id: ID of conversation to load

        Returns:
            True if loaded successfully
        """
        if self.history.load_conversation(conv_id):
            # Load messages from file
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
