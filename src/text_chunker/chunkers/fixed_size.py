"""Fixed size text chunker implementation."""

from typing import List

from ..core.base import BaseChunker
from ..core.metadata import TextChunk, ChunkMetadata
from ..core.exceptions import InvalidChunkSizeError


class FixedSizeChunker(BaseChunker):
    """Chunks text into fixed-size pieces."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 100, **kwargs):
        """
        Initialize fixed-size chunker.

        Args:
            chunk_size: Maximum size of each chunk in characters
            overlap: Number of overlapping characters between chunks

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

    def chunk_text(self, text: str, source_document: str) -> List[TextChunk]:
        """Chunk text into fixed-size pieces with optional overlap."""
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))

            # Try to break at word boundaries
            if end < len(text):
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space

            chunk_content = text[start:end].strip()

            if chunk_content:
                metadata = ChunkMetadata(
                    chunk_id=f"{source_document}_{chunk_index}",
                    source_document=source_document,
                    chunk_index=chunk_index,
                    start_position=start,
                    end_position=end,
                    chunk_size=len(chunk_content),
                    token_count=self.count_tokens(chunk_content),
                    overlap_with_previous=chunk_index > 0 and self.overlap > 0
                )

                chunks.append(TextChunk(chunk_content, metadata))
                chunk_index += 1

            start = end - self.overlap if self.overlap > 0 else end

        return chunks
