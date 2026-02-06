"""Model router for switching between different LLM providers."""

from typing import Literal
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from src.config import settings


class ModelRouter:
    """Routes requests to appropriate LLM provider."""

    def __init__(self, provider: Literal["openai", "anthropic"] = "openai"):
        """Initialize model router.
        
        Args:
            provider: LLM provider to use (openai or anthropic)
        """
        self.provider = provider
        self._model_cache: dict[str, BaseChatModel] = {}

    def get_model(
        self,
        provider: Literal["openai", "anthropic"] | None = None,
        temperature: float = 0.7,
        streaming: bool = False,
    ) -> BaseChatModel:
        """Get LLM model instance.
        
        Args:
            provider: Override default provider
            temperature: Model temperature (0.0 to 1.0)
            streaming: Enable streaming responses
            
        Returns:
            Configured LLM model instance
        """
        provider = provider or self.provider
        cache_key = f"{provider}_{temperature}_{streaming}"

        if cache_key not in self._model_cache:
            self._model_cache[cache_key] = self._create_model(provider, temperature, streaming)

        return self._model_cache[cache_key]

    def _create_model(
        self,
        provider: Literal["openai", "anthropic"],
        temperature: float,
        streaming: bool,
    ) -> BaseChatModel:
        """Create a new LLM model instance.
        
        Args:
            provider: LLM provider
            temperature: Model temperature
            streaming: Enable streaming
            
        Returns:
            New LLM model instance
            
        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        if provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            return ChatOpenAI(
                model=settings.openai_model,
                temperature=temperature,
                streaming=streaming,
                api_key=settings.openai_api_key,
            )
        elif provider == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("Anthropic API key not configured")
            return ChatAnthropic(
                model=settings.anthropic_model,
                temperature=temperature,
                streaming=streaming,
                api_key=settings.anthropic_api_key,
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def switch_provider(self, provider: Literal["openai", "anthropic"]) -> None:
        """Switch to a different LLM provider.
        
        Args:
            provider: New provider to use
        """
        self.provider = provider
