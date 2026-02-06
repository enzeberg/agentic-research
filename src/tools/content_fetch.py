"""Content fetching tool for web pages."""

import requests
from bs4 import BeautifulSoup
from typing import Any


class ContentFetchTool:
    """Fetches and processes web page content."""

    def __init__(self, timeout: int = 10):
        """Initialize content fetch tool.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch(self, url: str) -> dict[str, Any]:
        """Fetch content from URL.
        
        Args:
            url: URL to fetch
            
        Returns:
            Dictionary with title, text content, and metadata
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract title
            title = soup.title.string if soup.title else "No title"
            
            # Extract text
            text = soup.get_text(separator="\n", strip=True)
            
            return {
                "url": url,
                "title": title,
                "content": text,
                "status": "success",
                "length": len(text),
            }
        except Exception as e:
            return {
                "url": url,
                "status": "error",
                "error": str(e),
            }

    def fetch_multiple(self, urls: list[str]) -> list[dict[str, Any]]:
        """Fetch content from multiple URLs.
        
        Args:
            urls: List of URLs to fetch
            
        Returns:
            List of fetch results
        """
        return [self.fetch(url) for url in urls]

    def extract_main_content(self, url: str, max_length: int = 5000) -> str:
        """Extract main content from URL with length limit.
        
        Args:
            url: URL to fetch
            max_length: Maximum content length
            
        Returns:
            Extracted content string
        """
        result = self.fetch(url)
        
        if result["status"] == "error":
            return f"Error fetching {url}: {result['error']}"
        
        content = result["content"]
        if len(content) > max_length:
            content = content[:max_length] + "..."
        
        return f"Title: {result['title']}\nURL: {url}\n\n{content}"
