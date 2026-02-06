"""RAG agent for document retrieval and knowledge management."""

from typing import Any
from langchain_core.language_models import BaseChatModel

from src.rag.retriever import DocumentRetriever


class RAGAgent:
    """Agent responsible for RAG operations."""

    def __init__(
        self,
        llm: BaseChatModel,
        retriever: DocumentRetriever | None = None,
        embedding_provider: str = "openai",
    ):
        """Initialize RAG agent.
        
        Args:
            llm: Language model to use
            retriever: Document retriever
            embedding_provider: Embedding provider
        """
        self.llm = llm
        self.retriever = retriever or DocumentRetriever(
            embedding_provider=embedding_provider
        )

    async def add_documents(
        self,
        documents: list[dict[str, Any]],
    ) -> list[str]:
        """Add documents to the knowledge base.
        
        Args:
            documents: Documents to add
            
        Returns:
            List of document IDs
        """
        return self.retriever.add_documents(documents)

    async def retrieve_context(
        self,
        query: str,
        k: int = 4,
    ) -> str:
        """Retrieve relevant context for a query.
        
        Args:
            query: Query text
            k: Number of documents to retrieve
            
        Returns:
            Formatted context string
        """
        return self.retriever.get_context(query, k=k)

    async def answer_with_rag(
        self,
        query: str,
        k: int = 4,
    ) -> dict[str, Any]:
        """Answer a query using RAG.
        
        Args:
            query: Query to answer
            k: Number of documents to retrieve
            
        Returns:
            Answer with sources
        """
        # Retrieve relevant context
        context = await self.retrieve_context(query, k=k)
        
        # Generate answer using LLM
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful research assistant. Answer the question based on the provided context."),
            ("user", "Context:\n{context}\n\nQuestion: {query}\n\nProvide a detailed answer based on the context."),
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"context": context, "query": query})
        
        return {
            "query": query,
            "answer": response.content,
            "context": context,
        }

    def clear_knowledge_base(self) -> None:
        """Clear all documents from the knowledge base."""
        self.retriever.clear()
