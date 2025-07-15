# Text Chunker

A comprehensive Python library for text chunking optimized for embedding generation and RAG applications.

## Features

- Multiple chunking strategies (fixed-size, sentence-based, paragraph-based, recursive, sliding window)
- Token-aware processing with tiktoken integration
- Rich metadata for each chunk
- Optimized for embedding models
- Easy-to-use API
- Comprehensive test coverage

## Installation

```bash
pip install text-chunker
```

Or with Poetry:

```bash
poetry add text-chunker
```

## Quick Start

```python
from text_chunker import DocumentChunker, ChunkingStrategy

# Create a chunker
chunker = DocumentChunker(
    strategy=ChunkingStrategy.RECURSIVE,
    chunk_size=1000,
    overlap=200
)

# Chunk your text
chunks = chunker.chunk_document(text, "document_id")

# Get statistics
stats = chunker.get_chunk_stats(chunks)
print(f"Created {stats['total_chunks']} chunks")
```

## Documentation

Full documentation is available at [text-chunker.readthedocs.io](https://text-chunker.readthedocs.io)

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
