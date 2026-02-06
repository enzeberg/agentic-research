"""Tests for memory system."""

import pytest
from src.memory import WorkingMemory, ShortTermMemory, MemoryManager


def test_working_memory():
    """Test working memory operations."""
    memory = WorkingMemory(max_size=3)
    
    # Add items
    memory.add("query", "test query")
    memory.add("result", {"data": "test"})
    
    assert len(memory) == 2
    
    # Get recent items
    recent = memory.get_recent(1)
    assert len(recent) == 1
    assert recent[0]["type"] == "result"
    
    # Get by type
    queries = memory.get_by_type("query")
    assert len(queries) == 1
    assert queries[0]["content"] == "test query"
    
    # Clear
    memory.clear()
    assert len(memory) == 0


def test_short_term_memory():
    """Test short-term memory operations."""
    memory = ShortTermMemory(max_size=5)
    
    # Save session
    memory.save_session(
        query="test query",
        plan={"objective": "test"},
        results=[{"data": "test"}],
        report="test report"
    )
    
    assert len(memory) == 1
    
    # Get recent sessions
    sessions = memory.get_recent_sessions(1)
    assert len(sessions) == 1
    assert sessions[0]["query"] == "test query"
    
    # Find similar queries
    memory.save_session(
        query="another test query",
        plan={},
        results=[],
        report=""
    )
    
    similar = memory.find_similar_queries("test", top_k=2)
    assert len(similar) == 2


def test_memory_manager():
    """Test memory manager."""
    manager = MemoryManager(working_memory_size=3, short_term_memory_size=5)
    
    # Add to working memory
    manager.add_to_working("query", "test")
    assert len(manager.working_memory) == 1
    
    # Save session
    manager.save_session(
        query="test",
        plan={},
        results=[],
        report="test report"
    )
    assert len(manager.short_term_memory) == 1
    
    # Get context
    context = manager.get_context()
    assert "working_memory" in context
    assert "short_term_memory" in context
    
    # Clear working memory
    manager.clear_working_memory()
    assert len(manager.working_memory) == 0
    assert len(manager.short_term_memory) == 1
