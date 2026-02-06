"""Document processing utilities."""

from typing import Any
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentProcessor:
    """Processes documents for RAG and analysis."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """Initialize document processor.
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def split_text(self, text: str) -> list[str]:
        """Split text into chunks.
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        return self.text_splitter.split_text(text)

    def process_document(
        self,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Process document into chunks with metadata.
        
        Args:
            content: Document content
            metadata: Document metadata
            
        Returns:
            List of document chunks with metadata
        """
        chunks = self.split_text(content)
        metadata = metadata or {}
        
        return [
            {
                "content": chunk,
                "metadata": {**metadata, "chunk_index": i},
            }
            for i, chunk in enumerate(chunks)
        ]

    def extract_key_points(self, text: str, max_points: int = 5) -> list[str]:
        """Extract key points from text (simple sentence-based extraction).
        
        Args:
            text: Text to analyze
            max_points: Maximum number of key points
            
        Returns:
            List of key points
        """
        # Simple sentence splitting
        sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]
        
        # Return first max_points sentences as key points
        return sentences[:max_points]

    def summarize_content(self, content: str, max_length: int = 500) -> str:
        """Create a simple summary of content.
        
        Args:
            content: Content to summarize
            max_length: Maximum summary length
            
        Returns:
            Summary string
        """
        if len(content) <= max_length:
            return content
        
        # Simple truncation with ellipsis
        return content[:max_length].rsplit(" ", 1)[0] + "..."
