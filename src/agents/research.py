"""Research agent for executing research tasks."""

from typing import Any
from langchain_core.language_models import BaseChatModel

from src.tools.web_search import TavilySearchTool
from src.tools.content_fetch import ContentFetchTool
from src.tools.document import DocumentProcessor


class ResearchAgent:
    """Agent responsible for executing research tasks."""

    def __init__(
        self,
        llm: BaseChatModel,
        search_tool: TavilySearchTool | None = None,
        fetch_tool: ContentFetchTool | None = None,
    ):
        """Initialize research agent.
        
        Args:
            llm: Language model to use
            search_tool: Web search tool
            fetch_tool: Content fetch tool
        """
        self.llm = llm
        self.search_tool = search_tool or TavilySearchTool()
        self.fetch_tool = fetch_tool or ContentFetchTool()
        self.doc_processor = DocumentProcessor()

    async def execute_search(
        self,
        query: str,
        max_results: int = 5,
    ) -> dict[str, Any]:
        """Execute web search for a query.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Search results with metadata
        """
        results = self.search_tool.search(query, max_results=max_results)
        
        return {
            "query": query,
            "results": results.get("results", []),
            "answer": results.get("answer", ""),
            "source": "tavily_search",
        }

    async def fetch_content(
        self,
        urls: list[str],
    ) -> list[dict[str, Any]]:
        """Fetch content from URLs.
        
        Args:
            urls: List of URLs to fetch
            
        Returns:
            List of fetched content
        """
        return self.fetch_tool.fetch_multiple(urls)

    async def analyze_results(
        self,
        results: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Analyze research results.
        
        Args:
            results: Research results to analyze
            
        Returns:
            Analysis summary
        """
        # Combine all content
        all_content = []
        for result in results:
            if "content" in result:
                all_content.append(result["content"])
            elif "results" in result:
                for item in result["results"]:
                    if "content" in item:
                        all_content.append(item["content"])

        combined_text = "\n\n".join(all_content)
        
        # Extract key points
        key_points = self.doc_processor.extract_key_points(combined_text, max_points=10)
        
        return {
            "key_points": key_points,
            "total_sources": len(results),
            "content_length": len(combined_text),
        }

    async def execute_task(
        self,
        task: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute a research task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task results
        """
        task_type = task.get("type", "search")
        
        if task_type == "search":
            query = task.get("description", "")
            return await self.execute_search(query)
        
        elif task_type == "fetch":
            urls = task.get("urls", [])
            content = await self.fetch_content(urls)
            return {
                "task_id": task.get("id"),
                "content": content,
                "source": "content_fetch",
            }
        
        elif task_type == "analyze":
            results = task.get("results", [])
            analysis = await self.analyze_results(results)
            return {
                "task_id": task.get("id"),
                "analysis": analysis,
                "source": "analysis",
            }
        
        else:
            return {
                "task_id": task.get("id"),
                "error": f"Unknown task type: {task_type}",
            }

    def process_for_rag(
        self,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Process content for RAG storage.
        
        Args:
            content: Content to process
            metadata: Content metadata
            
        Returns:
            Processed document chunks
        """
        return self.doc_processor.process_document(content, metadata)
