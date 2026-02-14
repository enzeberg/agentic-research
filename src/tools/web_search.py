"""Web search tool using Tavily API."""

from typing import Any

from langchain_core.tools import tool
from tavily import TavilyClient

from src.config import settings


def _get_tavily_client() -> TavilyClient:
    """Get Tavily client instance."""
    if not settings.tavily_api_key:
        raise ValueError("Tavily API key not configured")
    return TavilyClient(api_key=settings.tavily_api_key)


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for information on a topic.

    Use this tool to find up-to-date information, facts, news, and research
    on any topic. Returns titles, URLs, and content snippets from web pages.

    Args:
        query: The search query to look up.
        max_results: Maximum number of results to return (default 5).
    """
    client = _get_tavily_client()

    try:
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
        )
    except Exception as e:
        return f"Search error: {e}"

    results = response.get("results", [])
    if not results:
        return "No results found."

    parts = []
    if response.get("answer"):
        parts.append(f"Quick Answer: {response['answer']}\n")

    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        url = result.get("url", "")
        content = result.get("content", "")[:400]
        parts.append(f"{i}. {title}\n   URL: {url}\n   {content}\n")

    return "\n".join(parts)


@tool
def get_search_urls(query: str, max_results: int = 5) -> str:
    """Search the web and return just the URLs for deeper content fetching.

    Use this when you want to find relevant pages to fetch full content from.

    Args:
        query: The search query to look up.
        max_results: Maximum number of URLs to return.
    """
    client = _get_tavily_client()

    try:
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="basic",
        )
    except Exception as e:
        return f"Search error: {e}"

    results = response.get("results", [])
    if not results:
        return "No results found."

    lines = []
    for r in results:
        lines.append(f"- {r.get('title', 'No title')}: {r.get('url', '')}")
    return "\n".join(lines)
