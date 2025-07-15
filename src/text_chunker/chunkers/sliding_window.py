"""Sliding window text chunker implementation."""

from typing import List

from ..core.base import BaseChunker
from ..core.metadata import TextChunk, ChunkMetadata
from ..core.exceptions import InvalidChunkSizeError


class SlidingWindowChunker(BaseChunker):
    """Creates overlapping chunks using a sliding window approach."""

    def __init__(self, window_size: int = 1000, step_size: int = 500, **kwargs):
        """
        Initialize sliding window chunker.

        Args:
            window_size: Size of each window in characters
            step_size: Step size for sliding the window

        Raises:
            InvalidChunkSizeError: If window_size or step_size are invalid
        """
        super().__init__(**kwargs)

        if window_size <= 0:
            raise InvalidChunkSizeError("window_size must be positive")
        if step_size <= 0:
            raise InvalidChunkSizeError("step_size must be positive")
        if step_size >= window_size:
            raise InvalidChunkSizeError("step_size should be less than window_size for overlap")

        self.window_size = window_size
        self.step_size = step_size

    def chunk_text(self, text: str, source_document: str) -> List[TextChunk]:
        """Create overlapping chunks using sliding window."""
        chunks = []
        chunk_index = 0

        for start in range(0, len(text), self.step_size):
            end = min(start + self.window_size, len(text))

            # Try to break at word boundaries
            if end < len(text):
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space

            chunk_content = text[start:end].strip()

            if chunk_content and len(chunk_content) > 50:  # Minimum chunk size
                metadata = ChunkMetadata(
                    chunk_id=f"{source_document}_{chunk_index}",
                    source_document=source_document,
                    chunk_index=chunk_index,
                    start_position=start,
                    end_position=end,
                    chunk_size=len(chunk_content),
                    token_count=self.count_tokens(chunk_content),
                    overlap_with_previous=chunk_index > 0
                )

                chunks.append(TextChunk(chunk_content, metadata))
                chunk_index += 1

            if end >= len(text):
                break

        return chunks
