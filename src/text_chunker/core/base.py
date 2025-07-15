"""Base abstract class for all chunkers."""

from abc import ABC, abstractmethod
from typing import List, Optional
import tiktoken

from .metadata import TextChunk
from .exceptions import TokenEncodingError


class BaseChunker(ABC):
    """Abstract base class for text chunkers."""

    def __init__(self, encoding_name: str = "cl100k_base"):
        """
        Initialize the chunker with token encoding.

        Args:
            encoding_name: Name of the tiktoken encoding to use

        Raises:
            TokenEncodingError: If encoding cannot be loaded
        """
        try:
            self.encoding = tiktoken.get_encoding(encoding_name)
        except Exception as e:
            raise TokenEncodingError(f"Failed to load encoding '{encoding_name}': {e}")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        try:
            return len(self.encoding.encode(text))
        except Exception:
            # Fallback to character-based approximation
            return len(text) // 4

    @abstractmethod
    def chunk_text(self, text: str, source_document: str) -> List[TextChunk]:
        """
        Abstract method to chunk text.

        Args:
            text: Text to chunk
            source_document: Identifier for the source document

        Returns:
            List of TextChunk objects
        """
        pass