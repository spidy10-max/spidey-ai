import openai
import os
from dotenv import load_dotenv
from spidey.logger import brain_logger, log_error, log_provider_switch

load_dotenv()


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
        if provider_name not in PROVIDERS:
            raise ValueError(
                f"Unknown provider: {provider_name}. "
                f"Available: {list(PROVIDERS.keys())}"
            )

        self.provider_name = provider_name
        self.config = PROVIDERS[provider_name]
        self.client = self._create_client()
        brain_logger.info(f"Provider initialized: {self.config['name']}")

    def _create_client(self):
        """Create OpenAI-compatible client"""
        api_key_env = self.config["api_key_env"]

        if api_key_env:
            api_key = os.getenv(api_key_env)
            if not api_key:
                error_msg = f"API key not found! Set {api_key_env} in .env"
                log_error(error_msg, "Provider._create_client")
                raise ValueError(error_msg)
        else:
            api_key = "ollama"

        return openai.OpenAI(
            api_key=api_key,
            base_url=self.config["base_url"]
        )

    def chat(self, messages, temperature=0.7, max_tokens=1024):
        """Send messages and get response"""
        try:
            brain_logger.debug(
                f"Sending {len(messages)} messages to {self.config['name']}"
            )

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

            brain_logger.debug(
                f"Response received: {result['total_tokens']} tokens"
            )

            return result

        except Exception as e:
            log_error(str(e), f"Provider.chat ({self.config['name']})")
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
    """Manages multiple providers and switching"""

    def __init__(self, default_provider="groq"):
        self.current_provider_name = default_provider
        self.current_provider = AIProvider(default_provider)

    def switch_provider(self, provider_name):
        """Switch to different provider"""
        try:
            old_name = self.current_provider_name
            new_provider = AIProvider(provider_name)
            self.current_provider = new_provider
            self.current_provider_name = provider_name
            log_provider_switch(old_name, provider_name)
            return True
        except ValueError as e:
            log_error(str(e), "ProviderManager.switch")
            print(f"❌ Error: {e}")
            return False

    def chat(self, messages, temperature=0.7, max_tokens=1024):
        """Send chat to current provider"""
        return self.current_provider.chat(messages, temperature, max_tokens)

    def get_current_info(self):
        """Get current provider info"""
        return self.current_provider.get_info()

    def get_current_name(self):
        """Get current provider name"""
        return self.current_provider_name

    @staticmethod
    def list_providers():
        """List all providers"""
        return PROVIDERS

    @staticmethod
    def get_available_providers():
        """Get providers with API keys"""
        available = []
        for key, config in PROVIDERS.items():
            api_key_env = config["api_key_env"]
            if api_key_env is None:
                available.append(key)
            elif os.getenv(api_key_env):
                available.append(key)
        return available