"""
Spidey AI — Multi-Provider System
Switch between different AI providers easily!
Supported: Groq, OpenAI, DeepSeek, Ollama
"""
import os
import openai
from dotenv import load_dotenv

load_dotenv()

from spidey.logger import get_logger

logger = get_logger(__name__)


# All available providers and their settings
PROVIDERS = {
    "groq": {
        "name": "Groq (Llama 3.1)",
        "api_key_env": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.1-8b-instant",
        "description": "Free, super fast, Llama 3.1 model",
        "free": True
    },
    "groq-large": {
        "name": "Groq (Llama 70B)",
        "api_key_env": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.3-70b-versatile",
        "description": "Free, powerful 70B model",
        "free": True
    },
    "groq-mixtral": {
        "name": "Groq (Mixtral)",
        "api_key_env": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "model": "mixtral-8x7b-32768",
        "description": "Free, good for coding tasks",
        "free": True
    },
    "openai": {
        "name": "OpenAI (GPT-4o-mini)",
        "api_key_env": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
        "description": "Paid, fast and smart, most popular",
        "free": False
    },
    "deepseek": {
        "name": "DeepSeek (V3)",
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
        "description": "Very cheap, great for coding",
        "free": False
    },
    "ollama": {
        "name": "Ollama (Local)",
        "api_key_env": None,
        "base_url": "http://localhost:11434/v1",
        "model": "llama3.2",
        "description": "Free, runs locally, no internet needed",
        "free": True
    }
}


class AIProvider:
    """Manages a single AI provider connection"""

    def __init__(self, provider_name="groq"):
        """
        Initialize an AI provider

        Args:
            provider_name: Key from PROVIDERS dict
        """
        if provider_name not in PROVIDERS:
            raise ValueError(
                f"Unknown provider: {provider_name}. "
                f"Available: {list(PROVIDERS.keys())}"
            )

        self.provider_name = provider_name
        self.config = PROVIDERS[provider_name]
        logger.info("Initializing AIProvider: %s", provider_name)
        self.client = self._create_client()

    def _create_client(self):
        """Create OpenAI-compatible client for this provider"""
        api_key_env = self.config["api_key_env"]

        if api_key_env:
            api_key = os.getenv(api_key_env)
            if not api_key:
                logger.error("Missing API key for provider %s (%s)", self.provider_name, api_key_env)
                raise ValueError(
                    f"API key not found! Set {api_key_env} in your .env file"
                )
        else:
            api_key = "ollama"
            logger.debug("Using local Ollama provider without API key")

        return openai.OpenAI(
            api_key=api_key,
            base_url=self.config["base_url"]
        )

    def chat(self, messages, temperature=0.7, max_tokens=1024):
        """
        Send messages to this provider and get response

        Args:
            messages: List of message dicts
            temperature: Creativity level
            max_tokens: Max response length

        Returns:
            dict with 'content', 'model', 'tokens' info
        """
        logger.debug(
            "Provider chat request: provider=%s model=%s temperature=%s max_tokens=%s messages=%s",
            self.provider_name,
            self.config["model"],
            temperature,
            max_tokens,
            len(messages)
        )

        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            result = {
                "content": response.choices[0].message.content,
                "model": response.model,
                "provider": self.provider_name,
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason
            }

            logger.info(
                "Provider response received: provider=%s model=%s tokens=%s finish=%s",
                self.provider_name,
                result["model"],
                result["total_tokens"],
                result["finish_reason"]
            )
            return result

        except Exception as e:
            logger.exception("Provider error for %s", self.provider_name)
            return {
                "content": f"Error from {self.config['name']}: {str(e)}",
                "model": self.config["model"],
                "provider": self.provider_name,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "finish_reason": "error"
            }

    def get_info(self):
        """Get provider info"""
        return {
            "name": self.config["name"],
            "model": self.config["model"],
            "description": self.config["description"],
            "free": self.config["free"]
        }


class ProviderManager:
    """Manages multiple AI providers and switching between them"""

    def __init__(self, default_provider="groq"):
        """
        Initialize provider manager

        Args:
            default_provider: Which provider to start with
        """
        logger.info("Creating ProviderManager with default provider=%s", default_provider)
        self.current_provider_name = default_provider
        self.current_provider = AIProvider(default_provider)

    def switch_provider(self, provider_name):
        """
        Switch to a different AI provider

        Args:
            provider_name: Key from PROVIDERS dict

        Returns:
            True if switched successfully, False otherwise
        """
        logger.info("Switching provider from %s to %s", self.current_provider_name, provider_name)
        try:
            new_provider = AIProvider(provider_name)
            self.current_provider = new_provider
            self.current_provider_name = provider_name
            logger.info("Provider switched to %s", provider_name)
            return True
        except ValueError as e:
            logger.warning("Provider switch failed: %s", e)
            print(f"❌ Error: {e}")
            return False

    def chat(self, messages, temperature=0.7, max_tokens=1024):
        """Send chat to current provider"""
        return self.current_provider.chat(
            messages, temperature, max_tokens
        )

    def get_current_info(self):
        """Get current provider info"""
        return self.current_provider.get_info()

    def get_current_name(self):
        """Get current provider name"""
        return self.current_provider_name

    @staticmethod
    def list_providers():
        """List all available providers"""
        return PROVIDERS

    @staticmethod
    def get_available_providers():
        """Get providers that have API keys configured"""
        available = []
        for key, config in PROVIDERS.items():
            api_key_env = config["api_key_env"]
            if api_key_env is None:
                available.append(key)
            elif os.getenv(api_key_env):
                available.append(key)
        return available
