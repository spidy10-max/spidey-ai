"""
Spidey AI - Configuration File
Saari settings yahan rakhi jati hain
"""

class Settings:
    # App Info
    APP_NAME: str = "Spidey AI"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Personal AI Assistant - 60 Day Build"
    
    # Server Settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # AI Settings (Week 2 mein use honge)
    DEFAULT_AI_PROVIDER: str = "openai"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7
    
    # Developer Info
    CREATOR: str = "Kashan"


# Single instance
settings = Settings()