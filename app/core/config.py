"""
Configuration management for Dadd-E
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Keys
    openai_api_key: str
    deepgram_api_key: str
    composio_api_key: str

    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_key: str

    # Redis
    redis_url: str = "redis://localhost:6379"
    redis_password: str = ""

    # Omi Device
    omi_device_mac: str = ""
    omi_audio_char_uuid: str = "19B10001-E8F2-537E-4F6C-D104768A1214"

    # Application
    app_name: str = "Dadd-E"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    # Wake Word
    wake_word: str = "dadd-e"

    # Models
    openai_model: str = "gpt-4o"
    vision_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-large"

    # Deepgram Voice Configuration
    deepgram_tts_voice: str = "aura-asteria-en"
    deepgram_tts_model: str = "aura-asteria-en"

    # Feature Flags
    enable_vision: bool = True
    enable_voice_stt: bool = True
    enable_voice_tts: bool = True
    enable_app_integrations: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
