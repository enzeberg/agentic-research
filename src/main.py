"""Main entry point for the Deep Research system."""

from typing import Any
import logging

from src.config import ResearchConfig, settings
from src.workflows import ResearchWorkflow
from src.memory import MemoryManager

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DeepResearchSystem:
    """Main system that orchestrates deep research.

    Architecture:
        - Planner (LLM chain): creates a structured research plan.
        - Research Agent (ReAct agent): autonomously searches the web and
          gathers information using tools.
        - Report Generator (LLM chain): synthesizes findings into a report.
    """

    def __init__(self, config: ResearchConfig | None = None):
        self.config = config or ResearchConfig(
            llm_provider=settings.default_llm_provider,
        )
        self.memory_manager = MemoryManager()

        logger.info(
            "Initialized research system (provider=%s)",
            self.config.llm_provider,
        )

    async def research(
        self,
        query: str,
        llm_provider: str | None = None,
    ) -> dict[str, Any]:
        """Execute deep research for a query.

        Args:
            query: The research question.
            llm_provider: Override default LLM provider for this session.

        Returns:
            Dict with keys: query, plan, findings, report, error, completed.
        """
        logger.info("Starting research: %s", query)

        if llm_provider:
            self.config.llm_provider = llm_provider

        workflow = ResearchWorkflow(
            config=self.config,
            memory_manager=self.memory_manager,
        )

        result = await workflow.run(query)

        if result.get("error"):
            logger.error("Research failed: %s", result["error"])
        else:
            logger.info("Research completed successfully")

        return result

    def get_memory_summary(self) -> dict[str, Any]:
        """Get a summary of the memory state."""
        return self.memory_manager.get_context()

    def clear_memory(self) -> None:
        """Clear all memory."""
        self.memory_manager.reset()
        logger.info("Memory cleared")

    def find_similar_research(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict[str, Any]]:
        """Find similar past research sessions."""
        return self.memory_manager.find_relevant_history(query, top_k)


async def main() -> None:
    """Example usage."""
    system = DeepResearchSystem()

    result = await system.research(
        query="What are the latest developments in quantum computing?",
    )

    if result.get("report"):
        print("\n" + "=" * 80)
        print("RESEARCH REPORT")
        print("=" * 80 + "\n")
        print(result["report"])
    else:
        print(f"Research failed: {result.get('error')}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
