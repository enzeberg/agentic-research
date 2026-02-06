"""Embedding management for RAG system."""

from typing import Literal
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings

from src.config import settings


class EmbeddingManager:
    """Manages embeddings for the RAG system."""

    def __init__(
        self,
        provider: Literal["openai", "huggingface"] = "openai",
        model: str | None = None,
    ):
        """Initialize embedding manager.
        
        Args:
            provider: Embedding provider (openai or huggingface)
            model: Specific model to use (uses defaults if None)
        """
        self.provider = provider
        self.model = model
        self._embeddings: Embeddings | None = None

    def get_embeddings(self) -> Embeddings:
        """Get embeddings instance.
        
        Returns:
            Configured embeddings instance
        """
        if self._embeddings is None:
            self._embeddings = self._create_embeddings()
        return self._embeddings

    def _create_embeddings(self) -> Embeddings:
        """Create embeddings instance based on provider.
        
        Returns:
            Embeddings instance
            
        Raises:
            ValueError: If provider is not supported
        """
        if self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            return OpenAIEmbeddings(
                model=self.model or "text-embedding-3-small",
                api_key=settings.openai_api_key,
            )
        elif self.provider == "huggingface":
            # Use local HuggingFace embeddings (no API key needed)
            return HuggingFaceEmbeddings(
                model_name=self.model or "sentence-transformers/all-MiniLM-L6-v2"
            )
        else:
            raise ValueError(f"Unsupported embedding provider: {self.provider}")
