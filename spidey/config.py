"""
Spidey AI — Configuration System
All settings in one place! Easy to change, easy to manage.
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
#                    DEFAULT SETTINGS
# ============================================================

# App Info
APP_NAME = "Spidey AI"
APP_VERSION = "0.4.0"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# ============================================================
#                    AI SETTINGS
# ============================================================

# Default AI Provider
DEFAULT_PROVIDER = "groq"

# AI Parameters
DEFAULT_TEMPERATURE = 0.7       # Creativity (0.0 - 2.0)
DEFAULT_MAX_TOKENS = 1024       # Max response length
DEFAULT_TOP_P = 1.0             # Nucleus sampling

# System Prompt — Spidey ki personality
SYSTEM_PROMPT = (
    "You are Spidey AI, a friendly, witty, and helpful AI assistant. "
    "You are smart, knowledgeable, and always ready to help. "
    "You sometimes use Spider-Man references but keep it professional. "
    "Keep your answers clear, concise, and helpful. "
    "If you don't know something, say so honestly."
)

# ============================================================
#                    FILE PATHS
# ============================================================

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CONVERSATIONS_DIR = os.path.join(DATA_DIR, "conversations")
LOGS_DIR = os.path.join(DATA_DIR, "logs")
CONFIG_FILE = os.path.join(DATA_DIR, "user_settings.json")

# ============================================================
#                    API KEYS
# ============================================================

API_KEYS = {
    "groq": os.getenv("GROQ_API_KEY"),
    "openai": os.getenv("OPENAI_API_KEY"),
    "anthropic": os.getenv("ANTHROPIC_API_KEY"),
    "deepseek": os.getenv("DEEPSEEK_API_KEY"),
    "google": os.getenv("GOOGLE_API_KEY"),
}

# ============================================================
#                 USER SETTINGS (Saveable)
# ============================================================

# Default user settings (can be changed at runtime)
DEFAULT_USER_SETTINGS = {
    "provider": DEFAULT_PROVIDER,
    "temperature": DEFAULT_TEMPERATURE,
    "max_tokens": DEFAULT_MAX_TOKENS,
    "top_p": DEFAULT_TOP_P,
    "system_prompt": SYSTEM_PROMPT,
    "theme": "dark",
    "language": "english",
    "voice_enabled": False,
    "auto_save": True,
    "show_tokens": False,
    "username": "User"
}


class Settings:
    """
    User settings manager
    Load, save, and modify settings at runtime
    """

    def __init__(self):
        """Initialize settings — load from file or use defaults"""
        self._settings = DEFAULT_USER_SETTINGS.copy()
        self._ensure_directories()
        self.load()

    def _ensure_directories(self):
        """Make sure all required directories exist"""
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(CONVERSATIONS_DIR, exist_ok=True)
        os.makedirs(LOGS_DIR, exist_ok=True)

    def get(self, key, default=None):
        """
        Get a setting value

        Args:
            key: Setting name
            default: Default value if not found

        Returns:
            Setting value
        """
        return self._settings.get(key, default)

    def set(self, key, value):
        """
        Set a setting value and save

        Args:
            key: Setting name
            value: New value
        """
        self._settings[key] = value
        self.save()

    def get_all(self):
        """Get all settings as dict"""
        return self._settings.copy()

    def reset(self):
        """Reset all settings to defaults"""
        self._settings = DEFAULT_USER_SETTINGS.copy()
        self.save()

    def save(self):
        """Save settings to JSON file"""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            if DEBUG:
                print(f"Error saving settings: {e}")

    def load(self):
        """Load settings from JSON file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    # Merge with defaults (in case new settings added)
                    for key, value in DEFAULT_USER_SETTINGS.items():
                        if key not in saved:
                            saved[key] = value
                    self._settings = saved
            except Exception as e:
                if DEBUG:
                    print(f"Error loading settings: {e}")
                self._settings = DEFAULT_USER_SETTINGS.copy()

    def __str__(self):
        """Pretty print settings"""
        lines = [f"\n{'='*50}", "   ⚙️  SPIDEY SETTINGS", f"{'='*50}"]
        for key, value in self._settings.items():
            lines.append(f"   {key}: {value}")
        lines.append(f"{'='*50}\n")
        return "\n".join(lines)


# Global settings instance
settings = Settings()
