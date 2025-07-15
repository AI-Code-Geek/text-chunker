"""Basic usage examples for text-chunker."""

from text_chunker import DocumentChunker, ChunkingStrategy, chunk_for_embeddings


def basic_chunking_example():
    """Demonstrate basic text chunking."""

    # Sample text
    text = """
    This is a sample document that will be chunked for embedding generation.
    
    The document contains multiple paragraphs and sections to demonstrate
    different chunking strategies.
    
    Each chunk should be appropriately sized for the embedding model while
    maintaining semantic coherence and context.
    """

    # Create chunker with recursive strategy
    chunker = DocumentChunker(
        strategy=ChunkingStrategy.RECURSIVE,
        chunk_size=500,
        overlap=100
    )

    # Chunk the document
    chunks = chunker.chunk_document(text, "sample_doc")

    # Print results
    print(f"Generated {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print(f"Content: {chunk.content[:100]}...")
        print(f"Tokens: {chunk.metadata.token_count}")
        print(f"Size: {chunk.metadata.chunk_size} characters")

    # Get statistics
    stats = chunker.get_chunk_stats(chunks)
    print(f"\nChunk Statistics: {stats}")


def embedding_optimized_example():
    """Demonstrate chunking optimized for embeddings."""

    text = "Your document text here..."

    # Use convenience function for embedding optimization
    chunks = chunk_for_embeddings(
        text,
        model_name="text-embedding-ada-002",
        max_tokens=8192
    )

    print(f"Created {len(chunks)} embedding-optimized chunks")


if __name__ == "__main__":
    basic_chunking_example()
    embedding_optimized_example()
