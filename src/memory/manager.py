"""Memory manager coordinating working and short-term memory."""

from typing import Any

from src.memory.working import WorkingMemory
from src.memory.short_term import ShortTermMemory
from src.config import settings


class MemoryManager:
    """Coordinates working memory and short-term memory."""

    def __init__(
        self,
        working_memory_size: int | None = None,
        short_term_memory_size: int | None = None,
    ):
        """Initialize memory manager.
        
        Args:
            working_memory_size: Size of working memory (uses config default if None)
            short_term_memory_size: Size of short-term memory (uses config default if None)
        """
        self.working_memory = WorkingMemory(
            max_size=working_memory_size or settings.max_working_memory_size
        )
        self.short_term_memory = ShortTermMemory(
            max_size=short_term_memory_size or settings.max_short_term_memory_size
        )

    def add_to_working(
        self, item_type: str, content: Any, metadata: dict[str, Any] | None = None
    ) -> None:
        """Add item to working memory.
        
        Args:
            item_type: Type of memory item
            content: Content to store
            metadata: Optional metadata
        """
        self.working_memory.add(item_type, content, metadata)

    def save_session(
        self,
        query: str,
        plan: dict[str, Any],
        results: list[dict[str, Any]],
        report: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Save completed session to short-term memory.
        
        Args:
            query: Research query
            plan: Research plan
            results: Research results
            report: Generated report
            metadata: Optional metadata
        """
        self.short_term_memory.save_session(query, plan, results, report, metadata)

    def get_context(self) -> dict[str, Any]:
        """Get full memory context.
        
        Returns:
            Dictionary containing working and short-term memory context
        """
        return {
            "working_memory": self.working_memory.get_recent(),
            "short_term_memory": self.short_term_memory.get_recent_sessions(n=3),
            "working_summary": self.working_memory.get_context_summary(),
            "short_term_summary": self.short_term_memory.get_summary(),
        }

    def find_relevant_history(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        """Find relevant past sessions for current query.
        
        Args:
            query: Current research query
            top_k: Number of relevant sessions to return
            
        Returns:
            List of relevant past sessions
        """
        return self.short_term_memory.find_similar_queries(query, top_k)

    def clear_working_memory(self) -> None:
        """Clear working memory (typically at session end)."""
        self.working_memory.clear()

    def reset(self) -> None:
        """Reset all memory."""
        self.working_memory.clear()
        self.short_term_memory.clear()
