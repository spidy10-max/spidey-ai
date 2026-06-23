"""
Spidey AI — Chat Brain
This is the core chat engine that talks to AI APIs
"""
import openai
import os
from dotenv import load_dotenv

load_dotenv()


class SpideyBrain:
    """Main AI chat class for Spidey"""

    def __init__(self):
        """Initialize the AI brain with Groq API"""
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

        # Conversation history
        self.messages = [self.system_prompt]

    def chat(self, user_message):
        """
        Send a message to AI and get response

        Args:
            user_message: What the user typed

        Returns:
            AI's response as string
        """
        # User ka message history mein add karo
        self.messages.append({
            "role": "user",
            "content": user_message
        })

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

            # AI ka jawab history mein add karo (yaad rakhne ke liye)
            self.messages.append({
                "role": "assistant",
                "content": ai_reply
            })

            return ai_reply

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            return error_msg

    def reset(self):
        """Reset conversation — naye siray se shuru karo"""
        self.messages = [self.system_prompt]

    def get_history_count(self):
        """Kitne messages hue ab tak"""
        # System message minus karo
        return len(self.messages) - 1
