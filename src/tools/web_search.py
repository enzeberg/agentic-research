"""Web search tool using Tavily API."""

from typing import Any
from tavily import TavilyClient

from src.config import settings


class TavilySearchTool:
    """Web search tool powered by Tavily API."""

    def __init__(self, api_key: str | None = None):
        """Initialize Tavily search tool.
        
        Args:
            api_key: Tavily API key (uses config default if None)
        """
        self.api_key = api_key or settings.tavily_api_key
        if not self.api_key:
            raise ValueError("Tavily API key not configured")
        self.client = TavilyClient(api_key=self.api_key)

    def search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: str = "advanced",
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
    ) -> dict[str, Any]:
        """Perform web search.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            search_depth: Search depth ('basic' or 'advanced')
            include_domains: List of domains to include
            exclude_domains: List of domains to exclude
            
        Returns:
            Search results with URLs, titles, and content
        """
        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth=search_depth,
                include_domains=include_domains,
                exclude_domains=exclude_domains,
            )
            return {
                "query": query,
                "results": response.get("results", []),
                "answer": response.get("answer", ""),
                "images": response.get("images", []),
            }
        except Exception as e:
            return {
                "query": query,
                "results": [],
                "error": str(e),
            }

    def get_search_context(
        self,
        query: str,
        max_results: int = 5,
    ) -> str:
        """Get search context as formatted string.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Formatted search context
        """
        results = self.search(query, max_results=max_results)
        
        if "error" in results:
            return f"Search error: {results['error']}"

        context_parts = [f"Search Query: {query}\n"]
        
        if results.get("answer"):
            context_parts.append(f"Quick Answer: {results['answer']}\n")

        context_parts.append("Search Results:")
        for i, result in enumerate(results.get("results", []), 1):
            context_parts.append(f"\n{i}. {result.get('title', 'No title')}")
            context_parts.append(f"   URL: {result.get('url', 'No URL')}")
            context_parts.append(f"   Content: {result.get('content', 'No content')[:300]}...")

        return "\n".join(context_parts)
