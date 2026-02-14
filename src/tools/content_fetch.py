"""Content fetching tool for web pages."""

import requests
from bs4 import BeautifulSoup

from langchain_core.tools import tool


@tool
def fetch_webpage(url: str, max_length: int = 5000) -> str:
    """Fetch and extract the main text content from a web page.

    Use this tool to read the full content of a web page when you need more
    detail than what web search snippets provide.

    Args:
        url: The URL of the web page to fetch.
        max_length: Maximum content length to return (default 5000 chars).
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        return f"Error fetching {url}: {e}"

    soup = BeautifulSoup(response.content, "html.parser")

    # Remove script and style elements
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else "No title"
    text = soup.get_text(separator="\n", strip=True)

    # Truncate if needed
    if len(text) > max_length:
        text = text[:max_length] + "\n...(truncated)"

    return f"Title: {title}\nURL: {url}\n\n{text}"
