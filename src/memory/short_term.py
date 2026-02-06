"""Short-term memory for recent research history."""

from typing import Any
from collections import deque
from datetime import datetime


class ShortTermMemory:
    """Manages short-term memory for recent research sessions."""

    def __init__(self, max_size: int = 10):
        """Initialize short-term memory.
        
        Args:
            max_size: Maximum number of sessions to keep
        """
        self.max_size = max_size
        self._sessions: deque[dict[str, Any]] = deque(maxlen=max_size)

    def save_session(
        self,
        query: str,
        plan: dict[str, Any],
        results: list[dict[str, Any]],
        report: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Save a completed research session.
        
        Args:
            query: Original research query
            plan: Research plan that was executed
            results: Research results collected
            report: Generated report
            metadata: Optional session metadata
        """
        session = {
            "query": query,
            "plan": plan,
            "results": results,
            "report": report,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        }
        self._sessions.append(session)

    def get_recent_sessions(self, n: int | None = None) -> list[dict[str, Any]]:
        """Get recent research sessions.
        
        Args:
            n: Number of sessions to retrieve (None for all)
            
        Returns:
            List of recent sessions
        """
        if n is None:
            return list(self._sessions)
        return list(self._sessions)[-n:]

    def find_similar_queries(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        """Find sessions with similar queries.
        
        Args:
            query: Query to match against
            top_k: Number of similar sessions to return
            
        Returns:
            List of similar sessions
        """
        # Simple keyword-based similarity (can be enhanced with embeddings)
        query_lower = query.lower()
        query_words = set(query_lower.split())

        scored_sessions = []
        for session in self._sessions:
            session_query = session["query"].lower()
            session_words = set(session_query.split())
            
            # Calculate Jaccard similarity
            intersection = len(query_words & session_words)
            union = len(query_words | session_words)
            similarity = intersection / union if union > 0 else 0
            
            scored_sessions.append((similarity, session))

        # Sort by similarity and return top_k
        scored_sessions.sort(key=lambda x: x[0], reverse=True)
        return [session for _, session in scored_sessions[:top_k]]

    def clear(self) -> None:
        """Clear all short-term memory."""
        self._sessions.clear()

    def get_summary(self) -> str:
        """Get a summary of short-term memory.
        
        Returns:
            Formatted summary string
        """
        if not self._sessions:
            return "No sessions in short-term memory."

        summary_parts = [f"Short-term Memory ({len(self._sessions)} sessions):"]
        for i, session in enumerate(self._sessions, 1):
            summary_parts.append(f"{i}. {session['query'][:80]}... ({session['timestamp']})")

        return "\n".join(summary_parts)

    def __len__(self) -> int:
        """Get number of sessions in short-term memory."""
        return len(self._sessions)
