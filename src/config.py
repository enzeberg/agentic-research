"""Configuration management for the Agentic Research System."""

from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # LLM Provider Configuration
    openai_api_key: str = Field(default="")
    anthropic_api_key: str = Field(default="")
    default_llm_provider: Literal["openai", "anthropic"] = Field(default="openai")
    
    # Model Configuration
    openai_model: str = Field(default="gpt-4-turbo-preview")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022")
    
    # Search API
    tavily_api_key: str = Field(default="")
    
    # Vector Store Configuration
    chroma_persist_directory: str = Field(default="./data/chroma")
    
    # Memory Configuration
    max_short_term_memory_size: int = Field(default=10)
    max_working_memory_size: int = Field(default=5)
    
    # Application Settings
    log_level: str = Field(default="INFO")
    max_research_iterations: int = Field(default=5)


class ResearchConfig:
    """Configuration for a research session."""

    def __init__(
        self,
        llm_provider: Literal["openai", "anthropic"] = "openai",
        max_iterations: int = 5,
        enable_rag: bool = True,
        memory_enabled: bool = True,
        verbose: bool = False,
    ):
        """Initialize research configuration.
        
        Args:
            llm_provider: LLM provider to use (openai or anthropic)
            max_iterations: Maximum research iterations
            enable_rag: Enable RAG for document retrieval
            memory_enabled: Enable memory system
            verbose: Enable verbose logging
        """
        self.llm_provider = llm_provider
        self.max_iterations = max_iterations
        self.enable_rag = enable_rag
        self.memory_enabled = memory_enabled
        self.verbose = verbose


# Global settings instance
settings = Settings()
