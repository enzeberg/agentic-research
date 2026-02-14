"""Configuration management for the Deep Research system."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # LLM Provider Configuration
    openai_api_key: str = Field(default="")
    anthropic_api_key: str = Field(default="")
    default_llm_provider: Literal["openai", "anthropic"] = Field(default="openai")

    # Model Configuration
    openai_model: str = Field(default="gpt-4-turbo-preview")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022")

    # Search API
    tavily_api_key: str = Field(default="")

    # Memory Configuration
    max_short_term_memory_size: int = Field(default=10)
    max_working_memory_size: int = Field(default=5)

    # Application Settings
    log_level: str = Field(default="INFO")


class ResearchConfig:
    """Configuration for a single research session."""

    def __init__(
        self,
        llm_provider: Literal["openai", "anthropic"] = "openai",
        memory_enabled: bool = True,
        verbose: bool = False,
    ):
        self.llm_provider = llm_provider
        self.memory_enabled = memory_enabled
        self.verbose = verbose


# Global settings instance
settings = Settings()
