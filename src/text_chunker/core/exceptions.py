"""Custom exceptions for text chunking operations."""


class ChunkingError(Exception):
    """Base exception for all chunking-related errors."""
    pass


class InvalidChunkSizeError(ChunkingError):
    """Raised when chunk size parameters are invalid."""
    pass


class TokenEncodingError(ChunkingError):
    """Raised when token encoding fails."""
    pass


class DocumentProcessingError(ChunkingError):
    """Raised when document processing fails."""
    pass


class InvalidStrategyError(ChunkingError):
    """Raised when an invalid chunking strategy is specified."""
    pass


class EmptyDocumentError(ChunkingError):
    """Raised when trying to chunk an empty document."""
    pass