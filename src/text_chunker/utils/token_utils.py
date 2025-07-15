"""Token-related utility functions."""

from typing import List

from ..core.metadata import TextChunk, ChunkingStrategy
from ..document_chunker import DocumentChunker
from .preprocessing import preprocess_text


def chunk_for_embeddings(
        text: str,
        model_name: str = "text-embedding-ada-002",
        max_tokens: int = 8192
) -> List[TextChunk]:
    """
    Convenience function to chunk text optimally for embedding models.

    Args:
        text: Text to chunk
        model_name: Name of the embedding model
        max_tokens: Maximum tokens per chunk for the model

    Returns:
        List of optimized text chunks
    """
    # Adjust chunk size based on model
    if "ada-002" in model_name:
        chunk_size = min(max_tokens * 4, 6000)  # Conservative estimate
    else:
        chunk_size = min(max_tokens * 4, 4000)

    # Use recursive chunking for best results
    chunker = DocumentChunker(
        strategy=ChunkingStrategy.RECURSIVE,
        chunk_size=chunk_size,
        overlap=200
    )

    preprocessed_text = preprocess_text(text)
    return chunker.chunk_document(preprocessed_text, "document")


def estimate_tokens(text: str, model_name: str = "text-embedding-ada-002") -> int:
    """
    Estimate token count for a given text and model.

    Args:
        text: Text to estimate tokens for
        model_name: Name of the model

    Returns:
        Estimated token count
    """
    # This is a simplified estimation
    # In practice, you'd want to use the actual tokenizer for the model
    return len(text) // 4