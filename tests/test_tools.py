"""Tests for tool implementations."""

import pytest
from src.tools import DocumentProcessor


def test_document_processor():
    """Test document processing."""
    processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
    
    # Test text splitting
    text = "This is a test. " * 50  # Create long text
    chunks = processor.split_text(text)
    
    assert len(chunks) > 1
    assert all(len(chunk) <= 120 for chunk in chunks)  # Allow some overflow
    
    # Test document processing
    docs = processor.process_document(text, metadata={"source": "test"})
    
    assert len(docs) > 0
    assert all("content" in doc for doc in docs)
    assert all("metadata" in doc for doc in docs)
    assert all(doc["metadata"]["source"] == "test" for doc in docs)
    
    # Test key points extraction
    key_points = processor.extract_key_points(text, max_points=3)
    assert len(key_points) <= 3
    
    # Test summarization
    summary = processor.summarize_content(text, max_length=50)
    assert len(summary) <= 55  # Allow for ellipsis
