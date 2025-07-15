"""Tests for the DocumentChunker class."""

import pytest
from text_chunker import DocumentChunker, ChunkingStrategy
from text_chunker.core.exceptions import ChunkingError


class TestDocumentChunker:
    """Test cases for DocumentChunker."""

    def test_init_with_recursive_strategy(self):
        """Test initialization with recursive strategy."""
        chunker = DocumentChunker(ChunkingStrategy.RECURSIVE)
        assert chunker.strategy == ChunkingStrategy.RECURSIVE

    def test_init_with_invalid_strategy(self):
        """Test initialization with invalid strategy."""
        with pytest.raises(ChunkingError):
            DocumentChunker("invalid_strategy")

    def test_chunk_document_basic(self):
        """Test basic document chunking."""
        chunker = DocumentChunker(
            ChunkingStrategy.FIXED_SIZE,
            chunk_size=100,
            overlap=20
        )

        text = "This is a test document. " * 10
        chunks = chunker.chunk_document(text, "test_doc")

        assert len(chunks) > 0
        assert all(chunk.metadata.source_document == "test_doc" for chunk in chunks)

    def test_chunk_empty_document(self):
        """Test chunking empty document."""
        chunker = DocumentChunker(ChunkingStrategy.FIXED_SIZE)
        chunks = chunker.chunk_document("", "empty_doc")
        assert len(chunks) == 0

    def test_get_chunk_stats(self):
        """Test chunk statistics calculation."""
        chunker = DocumentChunker(ChunkingStrategy.FIXED_SIZE, chunk_size=50)
        text = "This is a test. " * 20
        chunks = chunker.chunk_document(text, "test_doc")

        stats = chunker.get_chunk_stats(chunks)

        assert "total_chunks" in stats
        assert "total_characters" in stats
        assert "avg_chunk_size" in stats
        assert stats["total_chunks"] == len(chunks)