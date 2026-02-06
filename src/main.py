"""Main entry point for the Agentic Research System."""

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


class AgenticResearchSystem:
    """Main system orchestrating the research process."""

    def __init__(
        self,
        config: ResearchConfig | None = None,
    ):
        """Initialize the research system.
        
        Args:
            config: Research configuration (uses defaults if None)
        """
        self.config = config or ResearchConfig(
            llm_provider=settings.default_llm_provider,
            max_iterations=settings.max_research_iterations,
        )
        
        # Initialize memory manager
        self.memory_manager = MemoryManager()
        
        logger.info(f"Initialized Agentic Research System with {self.config.llm_provider} provider")

    async def research(
        self,
        query: str,
        llm_provider: str | None = None,
    ) -> dict[str, Any]:
        """Execute research for a query.
        
        Args:
            query: Research query
            llm_provider: Override default LLM provider
            
        Returns:
            Research results including report
        """
        logger.info(f"Starting research for query: {query}")
        
        # Update config if provider specified
        if llm_provider:
            self.config.llm_provider = llm_provider
        
        # Create workflow
        workflow = ResearchWorkflow(
            config=self.config,
            memory_manager=self.memory_manager,
        )
        
        # Run workflow
        result = await workflow.run(query)
        
        if result.get("error"):
            logger.error(f"Research failed: {result['error']}")
        else:
            logger.info("Research completed successfully")
        
        return result

    def get_memory_summary(self) -> dict[str, Any]:
        """Get summary of memory state.
        
        Returns:
            Memory summary
        """
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
        """Find similar past research.
        
        Args:
            query: Query to match
            top_k: Number of results
            
        Returns:
            List of similar research sessions
        """
        return self.memory_manager.find_relevant_history(query, top_k)


async def main() -> None:
    """Example usage of the system."""
    # Initialize system
    system = AgenticResearchSystem()
    
    # Run research
    result = await system.research(
        query="What are the latest developments in quantum computing?",
        llm_provider="openai",
    )
    
    # Print report
    if result.get("report"):
        print("\n" + "="*80)
        print("RESEARCH REPORT")
        print("="*80 + "\n")
        print(result["report"])
    else:
        print(f"Research failed: {result.get('error')}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
