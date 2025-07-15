"""Main document chunker interface."""

import json
from typing import Dict, List, Any

from ..core.metadata import ChunkingStrategy, TextChunk, ChunkMetadata
from ..core.exceptions import ChunkingError, InvalidStrategyError, DocumentProcessingError
from ..chunkers.fixed_size import FixedSizeChunker
from ..chunkers.sentence_based import SentenceBasedChunker
from ..chunkers.paragraph_based import ParagraphBasedChunker
from ..chunkers.recursive import RecursiveChunker
from ..chunkers.sliding_window import SlidingWindowChunker


class DocumentChunker:
    """Main interface for document chunking."""

    def __init__(self, strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE, **kwargs):
        """
        Initialize document chunker.

        Args:
            strategy: Chunking strategy to use
            **kwargs: Additional parameters for the chosen strategy

        Raises:
            InvalidStrategyError: If strategy is not supported
            ChunkingError: If chunker initialization fails
        """
        self.strategy = strategy
        self.chunker = self._create_chunker(**kwargs)

    def _create_chunker(self, **kwargs):
        """Create chunker instance based on strategy."""
        chunker_map = {
            ChunkingStrategy.FIXED_SIZE: FixedSizeChunker,
            ChunkingStrategy.SENTENCE_BASED: SentenceBasedChunker,
            ChunkingStrategy.PARAGRAPH_BASED: ParagraphBasedChunker,
            ChunkingStrategy.RECURSIVE: RecursiveChunker,
            ChunkingStrategy.SLIDING_WINDOW: SlidingWindowChunker,
        }

        chunker_class = chunker_map.get(self.strategy)
        if not chunker_class:
            raise InvalidStrategyError(f"Unsupported chunking strategy: {self.strategy}")

        try:
            return chunker_class(**kwargs)
        except Exception as e:
            raise ChunkingError(f"Failed to create chunker: {e}")

    def chunk_document(self, text: str, source_document: str) -> List[TextChunk]:
        """
        Chunk a document into text chunks.

        Args:
            text: The document text to chunk
            source_document: Identifier for the source document

        Returns:
            List of TextChunk objects

        Raises:
            DocumentProcessingError: If document processing fails
        """
        if not isinstance(text, str):
            raise DocumentProcessingError("Text must be a string")

        if not text.strip():
            return []

        try:
            return self.chunker.chunk_text(text, source_document)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to chunk document '{source_document}': {e}")

    def chunk_documents(self, documents: Dict[str, str]) -> Dict[str, List[TextChunk]]:
        """
        Chunk multiple documents.

        Args:
            documents: Dictionary mapping document names to their text content

        Returns:
            Dictionary mapping document names to their chunks

        Raises:
            DocumentProcessingError: If any document processing fails
        """
        if not isinstance(documents, dict):
            raise DocumentProcessingError("Documents must be a dictionary")

        results = {}
        for doc_name, doc_text in documents.items():
            try:
                results[doc_name] = self.chunk_document(doc_text, doc_name)
            except Exception as e:
                raise DocumentProcessingError(f"Failed to process document '{doc_name}': {e}")

        return results

    def get_chunk_stats(self, chunks: List[TextChunk]) -> Dict[str, Any]:
        """
        Get statistics about the chunks.

        Args:
            chunks: List of text chunks

        Returns:
            Dictionary containing chunk statistics
        """
        if not chunks:
            return {
                "total_chunks": 0,
                "total_characters": 0,
                "total_tokens": 0,
                "avg_chunk_size": 0,
                "avg_token_count": 0,
                "min_chunk_size": 0,
                "max_chunk_size": 0,
                "min_token_count": 0,
                "max_token_count": 0,
            }

        chunk_sizes = [chunk.metadata.chunk_size for chunk in chunks]
        token_counts = [chunk.metadata.token_count for chunk in chunks]

        return {
            "total_chunks": len(chunks),
            "total_characters": sum(chunk_sizes),
            "total_tokens": sum(token_counts),
            "avg_chunk_size": sum(chunk_sizes) / len(chunk_sizes),
            "avg_token_count": sum(token_counts) / len(token_counts),
            "min_chunk_size": min(chunk_sizes),
            "max_chunk_size": max(chunk_sizes),
            "min_token_count": min(token_counts),
            "max_token_count": max(token_counts),
        }

    def save_chunks(self, chunks: List[TextChunk], filename: str) -> None:
        """
        Save chunks to a JSON file.

        Args:
            chunks: List of text chunks
            filename: Output filename

        Raises:
            DocumentProcessingError: If saving fails
        """
        try:
            chunk_data = [chunk.to_dict() for chunk in chunks]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(chunk_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to save chunks to '{filename}': {e}")

    def load_chunks(self, filename: str) -> List[TextChunk]:
        """
        Load chunks from a JSON file.

        Args:
            filename: Input filename

        Returns:
            List of TextChunk objects

        Raises:
            DocumentProcessingError: If loading fails
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                chunk_data = json.load(f)

            chunks = []
            for data in chunk_data:
                metadata = ChunkMetadata(**data['metadata'])
                chunks.append(TextChunk(data['content'], metadata))

            return chunks
        except Exception as e:
            raise DocumentProcessingError(f"Failed to load chunks from '{filename}': {e}")
