"""Metadata classes and enums for text chunks."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class ChunkingStrategy(Enum):
    """Available chunking strategies."""

    FIXED_SIZE = "fixed_size"
    SENTENCE_BASED = "sentence_based"
    PARAGRAPH_BASED = "paragraph_based"
    SEMANTIC_BASED = "semantic_based"
    RECURSIVE = "recursive"
    SLIDING_WINDOW = "sliding_window"


@dataclass
class ChunkMetadata:
    """Metadata for each text chunk."""

    chunk_id: str
    source_document: str
    chunk_index: int
    start_position: int
    end_position: int
    chunk_size: int
    token_count: int
    overlap_with_previous: bool = False
    semantic_section: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "chunk_id": self.chunk_id,
            "source_document": self.source_document,
            "chunk_index": self.chunk_index,
            "start_position": self.start_position,
            "end_position": self.end_position,
            "chunk_size": self.chunk_size,
            "token_count": self.token_count,
            "overlap_with_previous": self.overlap_with_previous,
            "semantic_section": self.semantic_section,
        }


@dataclass
class TextChunk:
    """Represents a single text chunk with its metadata."""

    content: str
    metadata: ChunkMetadata

    def to_dict(self) -> Dict[str, Any]:
        """Convert chunk to dictionary format."""
        return {
            "content": self.content,
            "metadata": self.metadata.to_dict(),
        }

    def __len__(self) -> int:
        """Return the length of the chunk content."""
        return len(self.content)

    def __str__(self) -> str:
        """Return a string representation of the chunk."""
        return f"TextChunk(id={self.metadata.chunk_id}, size={self.metadata.chunk_size})"