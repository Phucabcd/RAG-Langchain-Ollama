from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chroma_collection: str = "documents"
    api_base_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def documents_dir(self) -> Path:
        return PROJECT_ROOT / "data" / "documents"

    @property
    def chroma_dir(self) -> Path:
        return PROJECT_ROOT / "data" / "chroma"


@lru_cache
def get_settings() -> Settings:
    return Settings()
