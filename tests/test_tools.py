"""Tests for tool implementations."""

from src.tools.web_search import web_search, get_search_urls
from src.tools.content_fetch import fetch_webpage


def test_web_search_tool_exists():
    """Test that web_search tool is properly defined."""
    assert web_search.name == "web_search"
    assert "search" in web_search.description.lower()


def test_get_search_urls_tool_exists():
    """Test that get_search_urls tool is properly defined."""
    assert get_search_urls.name == "get_search_urls"


def test_fetch_webpage_tool_exists():
    """Test that fetch_webpage tool is properly defined."""
    assert fetch_webpage.name == "fetch_webpage"
    assert "url" in fetch_webpage.description.lower()
