"""Document retrieval system."""

from typing import Any

from src.rag.vectorstore import VectorStoreManager
from src.rag.embeddings import EmbeddingManager


class DocumentRetriever:
    """Handles document retrieval for RAG."""

    def __init__(
        self,
        embedding_provider: str = "openai",
        collection_name: str = "research_docs",
    ):
        """Initialize document retriever.
        
        Args:
            embedding_provider: Embedding provider to use
            collection_name: Vector store collection name
        """
        self.embedding_manager = EmbeddingManager(provider=embedding_provider)
        self.embeddings = self.embedding_manager.get_embeddings()
        self.vectorstore = VectorStoreManager(
            embeddings=self.embeddings,
            collection_name=collection_name,
        )

    def add_documents(
        self,
        documents: list[dict[str, Any]],
    ) -> list[str]:
        """Add documents to the retrieval system.
        
        Args:
            documents: List of documents with 'content' and optional 'metadata'
            
        Returns:
            List of document IDs
        """
        texts = [doc["content"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        return self.vectorstore.add_documents(texts, metadatas)

    def retrieve(
        self,
        query: str,
        k: int = 4,
        filter: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieve relevant documents for a query.
        
        Args:
            query: Query text
            k: Number of documents to retrieve
            filter: Metadata filter
            
        Returns:
            List of retrieved documents with scores
        """
        results = self.vectorstore.similarity_search(query, k=k, filter=filter)
        
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score,
            }
            for doc, score in results
        ]

    def get_context(
        self,
        query: str,
        k: int = 4,
        max_length: int = 2000,
    ) -> str:
        """Get formatted context for a query.
        
        Args:
            query: Query text
            k: Number of documents to retrieve
            max_length: Maximum total context length
            
        Returns:
            Formatted context string
        """
        results = self.retrieve(query, k=k)
        
        if not results:
            return "No relevant documents found."

        context_parts = ["Retrieved Context:"]
        current_length = 0

        for i, result in enumerate(results, 1):
            content = result["content"]
            if current_length + len(content) > max_length:
                # Truncate to fit max_length
                remaining = max_length - current_length
                content = content[:remaining] + "..."
                context_parts.append(f"\n{i}. {content}")
                break
            
            context_parts.append(f"\n{i}. {content}")
            current_length += len(content)

        return "\n".join(context_parts)

    def clear(self) -> None:
        """Clear all documents from the retrieval system."""
        self.vectorstore.clear()
