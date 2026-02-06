"""Working memory for current session context."""

from typing import Any
from collections import deque
from datetime import datetime


class WorkingMemory:
    """Manages working memory for the current research session."""

    def __init__(self, max_size: int = 5):
        """Initialize working memory.
        
        Args:
            max_size: Maximum number of items to keep in memory
        """
        self.max_size = max_size
        self._memory: deque[dict[str, Any]] = deque(maxlen=max_size)

    def add(self, item_type: str, content: Any, metadata: dict[str, Any] | None = None) -> None:
        """Add an item to working memory.
        
        Args:
            item_type: Type of memory item (e.g., 'query', 'result', 'plan')
            content: Content to store
            metadata: Optional metadata
        """
        memory_item = {
            "type": item_type,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        }
        self._memory.append(memory_item)

    def get_recent(self, n: int | None = None) -> list[dict[str, Any]]:
        """Get recent memory items.
        
        Args:
            n: Number of items to retrieve (None for all)
            
        Returns:
            List of recent memory items
        """
        if n is None:
            return list(self._memory)
        return list(self._memory)[-n:]

    def get_by_type(self, item_type: str) -> list[dict[str, Any]]:
        """Get memory items by type.
        
        Args:
            item_type: Type of items to retrieve
            
        Returns:
            List of matching memory items
        """
        return [item for item in self._memory if item["type"] == item_type]

    def clear(self) -> None:
        """Clear all working memory."""
        self._memory.clear()

    def get_context_summary(self) -> str:
        """Get a summary of current working memory context.
        
        Returns:
            Formatted summary string
        """
        if not self._memory:
            return "No items in working memory."

        summary_parts = ["Working Memory Context:"]
        for item in self._memory:
            summary_parts.append(f"- [{item['type']}] {str(item['content'])[:100]}")

        return "\n".join(summary_parts)

    def __len__(self) -> int:
        """Get number of items in working memory."""
        return len(self._memory)
