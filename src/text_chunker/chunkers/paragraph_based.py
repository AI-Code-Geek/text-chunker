"""Paragraph-based text chunker implementation."""

from typing import List

from ..core.base import BaseChunker
from ..core.metadata import TextChunk, ChunkMetadata
from ..core.exceptions import InvalidChunkSizeError


class ParagraphBasedChunker(BaseChunker):
    """Chunks text by paragraphs, combining them as needed."""

    def __init__(self, target_size: int = 1500, **kwargs):
        """
        Initialize paragraph-based chunker.

        Args:
            target_size: Target size for each chunk in characters

        Raises:
            InvalidChunkSizeError: If target_size is invalid
        """
        super().__init__(**kwargs)

        if target_size <= 0:
            raise InvalidChunkSizeError("target_size must be positive")

        self.target_size = target_size

    def chunk_text(self, text: str, source_document: str) -> List[TextChunk]:
        """Chunk text by paragraphs."""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        chunks = []
        chunk_index = 0
        current_chunk = []
        current_size = 0
        start_pos = 0

        for paragraph in paragraphs:
            paragraph_size = len(paragraph)

            if current_size + paragraph_size > self.target_size and current_chunk:
                # Create chunk from current paragraphs
                chunk_content = '\n\n'.join(current_chunk)
                end_pos = start_pos + len(chunk_content)

                metadata = ChunkMetadata(
                    chunk_id=f"{source_document}_{chunk_index}",
                    source_document=source_document,
                    chunk_index=chunk_index,
                    start_position=start_pos,
                    end_position=end_pos,
                    chunk_size=len(chunk_content),
                    token_count=self.count_tokens(chunk_content)
                )

                chunks.append(TextChunk(chunk_content, metadata))
                chunk_index += 1
                start_pos = end_pos
                current_chunk = []
                current_size = 0

            current_chunk.append(paragraph)
            current_size += paragraph_size

        # Handle remaining paragraphs
        if current_chunk:
            chunk_content = '\n\n'.join(current_chunk)
            end_pos = start_pos + len(chunk_content)

            metadata = ChunkMetadata(
                chunk_id=f"{source_document}_{chunk_index}",
                source_document=source_document,
                chunk_index=chunk_index,
                start_position=start_pos,
                end_position=end_pos,
                chunk_size=len(chunk_content),
                token_count=self.count_tokens(chunk_content)
            )

            chunks.append(TextChunk(chunk_content, metadata))

        return chunks