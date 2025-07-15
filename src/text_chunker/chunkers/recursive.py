"""Recursive text chunker implementation."""

from typing import List, Optional

from ..core.base import BaseChunker
from ..core.metadata import TextChunk, ChunkMetadata
from ..core.exceptions import InvalidChunkSizeError


class RecursiveChunker(BaseChunker):
    """Recursively chunks text using multiple separators."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 100,
                 separators: Optional[List[str]] = None, **kwargs):
        """
        Initialize recursive chunker.

        Args:
            chunk_size: Target chunk size in characters
            overlap: Overlap between chunks
            separators: List of separators to try in order

        Raises:
            InvalidChunkSizeError: If chunk_size or overlap are invalid
        """
        super().__init__(**kwargs)

        if chunk_size <= 0:
            raise InvalidChunkSizeError("chunk_size must be positive")
        if overlap < 0:
            raise InvalidChunkSizeError("overlap cannot be negative")
        if overlap >= chunk_size:
            raise InvalidChunkSizeError("overlap must be less than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def _split_text(self, text: str, separator: str) -> List[str]:
        """Split text by separator."""
        if separator:
            return text.split(separator)
        else:
            return list(text)

    def _merge_splits(self, splits: List[str], separator: str) -> List[str]:
        """Merge splits into chunks of appropriate size."""
        chunks = []
        current_chunk = []
        current_size = 0

        for split in splits:
            split_size = len(split)

            if current_size + split_size > self.chunk_size and current_chunk:
                chunks.append(separator.join(current_chunk))
                current_chunk = []
                current_size = 0

            current_chunk.append(split)
            current_size += split_size

        if current_chunk:
            chunks.append(separator.join(current_chunk))

        return chunks

    def chunk_text(self, text: str, source_document: str) -> List[TextChunk]:
        """Recursively chunk text."""
        final_chunks = []

        def _chunk_recursive(text_part: str, separator_index: int = 0) -> List[str]:
            if len(text_part) <= self.chunk_size:
                return [text_part]

            if separator_index >= len(self.separators):
                return [text_part[:self.chunk_size]]

            separator = self.separators[separator_index]
            splits = self._split_text(text_part, separator)
            merged = self._merge_splits(splits, separator)

            result = []
            for chunk in merged:
                if len(chunk) > self.chunk_size:
                    result.extend(_chunk_recursive(chunk, separator_index + 1))
                else:
                    result.append(chunk)

            return result

        text_chunks = _chunk_recursive(text)

        # Convert to TextChunk objects
        start_pos = 0
        for i, chunk_content in enumerate(text_chunks):
            if chunk_content.strip():
                end_pos = start_pos + len(chunk_content)

                metadata = ChunkMetadata(
                    chunk_id=f"{source_document}_{i}",
                    source_document=source_document,
                    chunk_index=i,
                    start_position=start_pos,
                    end_position=end_pos,
                    chunk_size=len(chunk_content),
                    token_count=self.count_tokens(chunk_content)
                )

                final_chunks.append(TextChunk(chunk_content, metadata))
                start_pos = end_pos

        return final_chunks