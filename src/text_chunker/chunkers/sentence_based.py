"""Sentence-based text chunker implementation."""

import re
from typing import List

from ..core.base import BaseChunker
from ..core.metadata import TextChunk, ChunkMetadata
from ..core.exceptions import InvalidChunkSizeError


class SentenceBasedChunker(BaseChunker):
    """Chunks text by sentences, grouping them to reach target size."""

    def __init__(self, target_size: int = 1000, max_sentences: int = 10, **kwargs):
        """
        Initialize sentence-based chunker.

        Args:
            target_size: Target size for each chunk in characters
            max_sentences: Maximum number of sentences per chunk

        Raises:
            InvalidChunkSizeError: If target_size or max_sentences are invalid
        """
        super().__init__(**kwargs)

        if target_size <= 0:
            raise InvalidChunkSizeError("target_size must be positive")
        if max_sentences <= 0:
            raise InvalidChunkSizeError("max_sentences must be positive")

        self.target_size = target_size
        self.max_sentences = max_sentences
        self.sentence_pattern = re.compile(r'[.!?]+\s+')

    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        sentences = self.sentence_pattern.split(text)
        return [s.strip() for s in sentences if s.strip()]

    def chunk_text(self, text: str, source_document: str) -> List[TextChunk]:
        """Chunk text by grouping sentences."""
        sentences = self.split_into_sentences(text)
        chunks = []
        chunk_index = 0
        current_chunk = []
        current_size = 0
        start_pos = 0

        for sentence in sentences:
            sentence_size = len(sentence)

            if (current_size + sentence_size > self.target_size and current_chunk) or \
                    len(current_chunk) >= self.max_sentences:

                # Create chunk from current sentences
                chunk_content = ' '.join(current_chunk)
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

            current_chunk.append(sentence)
            current_size += sentence_size

        # Handle remaining sentences
        if current_chunk:
            chunk_content = ' '.join(current_chunk)
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