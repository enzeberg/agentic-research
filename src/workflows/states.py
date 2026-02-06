"""State definitions for LangGraph workflows."""

from typing import TypedDict, Annotated, Any
from operator import add


class ResearchState(TypedDict):
    """State for the research workflow."""
    
    # Input
    query: str
    llm_provider: str
    
    # Planning
    plan: dict[str, Any]
    tasks: Annotated[list[dict[str, Any]], add]
    
    # Research
    search_results: Annotated[list[dict[str, Any]], add]
    documents: Annotated[list[dict[str, Any]], add]
    
    # RAG
    rag_context: str
    
    # Memory
    memory_context: dict[str, Any]
    
    # Output
    report: str
    
    # Control
    iteration: int
    max_iterations: int
    completed: bool
    error: str | None
