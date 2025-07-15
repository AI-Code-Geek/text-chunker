"""Text preprocessing utilities."""

import re


def preprocess_text(text: str) -> str:
    """
    Preprocess text before chunking.

    Args:
        text: Raw text to preprocess

    Returns:
        Preprocessed text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove page breaks and form feeds
    text = re.sub(r'[\f\v]+', '\n', text)

    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove multiple consecutive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def clean_text(text: str, remove_urls: bool = True, remove_emails: bool = True) -> str:
    """
    Clean text by removing URLs, emails, and other noise.

    Args:
        text: Text to clean
        remove_urls: Whether to remove URLs
        remove_emails: Whether to remove email addresses

    Returns:
        Cleaned text
    """
    if remove_urls:
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    if remove_emails:
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
