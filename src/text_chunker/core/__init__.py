"""Core components for text chunking."""

from .base import BaseChunker
from .metadata import ChunkMetadata, TextChunk, ChunkingStrategy
from .exceptions import (
    ChunkingError,
    InvalidChunkSizeError,
    TokenEncodingError,
    DocumentProcessingError
)

__all__ = [
    "BaseChunker",
    "ChunkMetadata",
    "TextChunk",
    "ChunkingStrategy",
    "ChunkingError",
    "InvalidChunkSizeError",
    "TokenEncodingError",
    "DocumentProcessingError",
]