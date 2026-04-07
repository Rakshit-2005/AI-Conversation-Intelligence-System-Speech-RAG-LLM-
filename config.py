"""
Configuration management for AI Conversation Intelligence System
"""

import os
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings management"""

    # Application
    APP_NAME: str = "AI Conversation Intelligence System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True

    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    MODELS_DIR: Path = PROJECT_ROOT / "models"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"

    # Speech Recognition
    WHISPER_MODEL: Literal["tiny", "base", "small", "medium", "large"] = "base"
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_FORMATS: list = ["wav", "mp3", "m4a", "flac", "ogg"]

    # Text Processing
    CHUNK_SIZE: int = 500  # Characters per chunk
    CHUNK_OVERLAP: int = 100  # Overlap between chunks
    MIN_CHUNK_SIZE: int = 100  # Minimum chunk size

    # Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    BATCH_SIZE: int = 32

    # Vector Database (FAISS)
    FAISS_INDEX_PATH: Path = PROJECT_ROOT / "models" / "faiss_index"
    FAISS_METADATA_PATH: Path = PROJECT_ROOT / "models" / "metadata.json"
    FAISS_ENABLE_GPU: bool = False

    # LLM Configuration
    LLM_PROVIDER: Literal["openai", "gemini"] = "openai"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4"  # or "gpt-3.5-turbo"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # LLM Parameters
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.9
    TOP_K: int = 40

    # RAG Configuration
    RETRIEVAL_TOP_K: int = 5  # Top-k chunks to retrieve
    SIMILARITY_THRESHOLD: float = 0.5
    CONTEXT_WINDOW_SIZE: int = 2000  # Max context to pass to LLM

    # Analysis Settings
    SENTIMENT_LABELS: list = ["positive", "neutral", "negative"]
    ACTION_ITEM_CONFIDENCE_THRESHOLD: float = 0.6

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # "json" or "standard"

    # Performance
    ENABLE_CACHING: bool = True
    CACHE_TTL: int = 3600  # 1 hour in seconds
    ENABLE_ASYNC_PROCESSING: bool = True
    MAX_WORKERS: int = 4

    # Timeouts
    TRANSCRIPTION_TIMEOUT: int = 300  # 5 minutes
    LLM_TIMEOUT: int = 120  # 2 minutes
    EMBEDDING_TIMEOUT: int = 60  # 1 minute

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create necessary directories
        self.LOGS_DIR.mkdir(exist_ok=True, parents=True)
        self.DATA_DIR.mkdir(exist_ok=True, parents=True)
        self.MODELS_DIR.mkdir(exist_ok=True, parents=True)


# Global settings instance
settings = Settings()

# Validate API keys
if settings.LLM_PROVIDER == "openai" and not settings.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

if settings.LLM_PROVIDER == "gemini" and not settings.GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")
