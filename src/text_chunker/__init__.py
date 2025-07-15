"""Text Chunker - A comprehensive text chunking library for embeddings."""

# Import all core components
from .core.metadata import ChunkingStrategy, TextChunk, ChunkMetadata
from .core.base import BaseChunker
from .core.exceptions import (
    ChunkingError,
    InvalidChunkSizeError,
    TokenEncodingError,
    DocumentProcessingError
)

# Import all chunker implementations
from .chunkers.fixed_size import FixedSizeChunker
from .chunkers.sentence_based import SentenceBasedChunker
from .chunkers.paragraph_based import ParagraphBasedChunker
from .chunkers.recursive import RecursiveChunker
from .chunkers.sliding_window import SlidingWindowChunker

# Import main interface
from .document_chunker import DocumentChunker

# Import utilities
from .utils.preprocessing import preprocess_text, clean_text
from .utils.token_utils import chunk_for_embeddings, estimate_tokens

# Package metadata
__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Public API - what gets imported with "from text_chunker import *"
__all__ = [
    # Core classes
    "DocumentChunker",
    "ChunkingStrategy",
    "TextChunk",
    "ChunkMetadata",
    "BaseChunker",

    # Individual chunkers
    "FixedSizeChunker",
    "SentenceBasedChunker",
    "ParagraphBasedChunker",
    "RecursiveChunker",
    "SlidingWindowChunker",

    # Utility functions
    "preprocess_text",
    "clean_text",
    "chunk_for_embeddings",
    "estimate_tokens",

    # Exceptions
    "ChunkingError",
    "InvalidChunkSizeError",
    "TokenEncodingError",
    "DocumentProcessingError",
]