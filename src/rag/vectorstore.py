"""Vector store management using Chroma."""

from typing import Any
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings

from src.config import settings


class VectorStoreManager:
    """Manages Chroma vector store for document retrieval."""

    def __init__(
        self,
        embeddings: Embeddings,
        collection_name: str = "research_docs",
        persist_directory: str | None = None,
    ):
        """Initialize vector store manager.
        
        Args:
            embeddings: Embedding model to use
            collection_name: Name of the collection
            persist_directory: Directory to persist data (uses config default if None)
        """
        self.embeddings = embeddings
        self.collection_name = collection_name
        self.persist_directory = persist_directory or settings.chroma_persist_directory
        
        # Initialize Chroma client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        
        # Initialize vector store
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=collection_name,
            embedding_function=embeddings,
        )

    def add_documents(
        self,
        texts: list[str],
        metadatas: list[dict[str, Any]] | None = None,
    ) -> list[str]:
        """Add documents to vector store.
        
        Args:
            texts: List of text documents
            metadatas: List of metadata dictionaries
            
        Returns:
            List of document IDs
        """
        return self.vectorstore.add_texts(texts=texts, metadatas=metadatas)

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: dict[str, Any] | None = None,
    ) -> list[tuple[Any, float]]:
        """Search for similar documents.
        
        Args:
            query: Query text
            k: Number of results to return
            filter: Metadata filter
            
        Returns:
            List of (document, score) tuples
        """
        return self.vectorstore.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter,
        )

    def get_retriever(self, k: int = 4):
        """Get a retriever for the vector store.
        
        Args:
            k: Number of documents to retrieve
            
        Returns:
            Retriever instance
        """
        return self.vectorstore.as_retriever(search_kwargs={"k": k})

    def delete_collection(self) -> None:
        """Delete the current collection."""
        self.client.delete_collection(name=self.collection_name)

    def clear(self) -> None:
        """Clear all documents from the collection."""
        self.delete_collection()
        # Recreate the collection
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
        )
