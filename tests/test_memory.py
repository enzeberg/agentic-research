"""Tests for the memory system."""

import pytest
from src.memory import WorkingMemory, ShortTermMemory, MemoryManager


def test_working_memory_add_and_retrieve():
    """Test adding and retrieving items from working memory."""
    memory = WorkingMemory(max_size=3)

    memory.add("query", "test query")
    memory.add("result", {"data": "test"})

    assert len(memory) == 2

    recent = memory.get_recent(1)
    assert len(recent) == 1
    assert recent[0]["type"] == "result"


def test_working_memory_overflow():
    """Test that working memory respects max size."""
    memory = WorkingMemory(max_size=2)

    memory.add("a", "first")
    memory.add("b", "second")
    memory.add("c", "third")

    assert len(memory) == 2
    items = memory.get_recent()
    assert items[0]["content"] == "second"
    assert items[1]["content"] == "third"


def test_working_memory_get_by_type():
    """Test filtering by item type."""
    memory = WorkingMemory(max_size=5)

    memory.add("query", "q1")
    memory.add("result", "r1")
    memory.add("query", "q2")

    queries = memory.get_by_type("query")
    assert len(queries) == 2
    assert queries[0]["content"] == "q1"


def test_working_memory_clear():
    """Test clearing memory."""
    memory = WorkingMemory(max_size=3)
    memory.add("query", "test")
    memory.clear()
    assert len(memory) == 0


def test_short_term_memory_save_and_retrieve():
    """Test saving and retrieving sessions."""
    memory = ShortTermMemory(max_size=5)

    memory.save_session(
        query="test query",
        plan={"objective": "test"},
        results=[{"data": "test"}],
        report="test report",
    )

    assert len(memory) == 1

    sessions = memory.get_recent_sessions(1)
    assert len(sessions) == 1
    assert sessions[0]["query"] == "test query"


def test_short_term_memory_find_similar():
    """Test finding similar queries."""
    memory = ShortTermMemory(max_size=5)

    memory.save_session(query="machine learning basics", plan={}, results=[], report="")
    memory.save_session(query="quantum computing news", plan={}, results=[], report="")
    memory.save_session(query="deep learning tutorial", plan={}, results=[], report="")

    similar = memory.find_similar_queries("learning", top_k=2)
    assert len(similar) == 2


def test_memory_manager_integration():
    """Test the memory manager coordinating both memory types."""
    manager = MemoryManager(working_memory_size=3, short_term_memory_size=5)

    manager.add_to_working("query", "test")
    assert len(manager.working_memory) == 1

    manager.save_session(query="test", plan={}, results=[], report="report")
    assert len(manager.short_term_memory) == 1

    context = manager.get_context()
    assert "working_memory" in context
    assert "short_term_memory" in context

    manager.clear_working_memory()
    assert len(manager.working_memory) == 0
    assert len(manager.short_term_memory) == 1

    manager.reset()
    assert len(manager.working_memory) == 0
    assert len(manager.short_term_memory) == 0
