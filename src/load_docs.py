"""
Load and clean policy documents from the data directory.
"""

import os
import re


def load_documents(data_dir: str) -> dict[str, str]:
    """
    Load all .txt files from the data directory.
    
    Args:
        data_dir: Path to directory containing policy documents
        
    Returns:
        Dictionary mapping filename to cleaned document text
    """
    documents = {}
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_text = f.read()
                # Clean the text: remove extra whitespace, normalize line breaks
                cleaned_text = clean_text(raw_text)
                documents[filename] = cleaned_text
    
    return documents


def clean_text(text: str) -> str:
    """
    Clean document text by removing extra whitespace and normalizing formatting.
    
    Why this matters:
    - Removes multiple consecutive newlines that can break chunking
    - Normalizes spaces to prevent embedding issues
    - Preserves structure while making text uniform
    
    Args:
        text: Raw document text
        
    Returns:
        Cleaned text ready for chunking
    """
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Replace multiple newlines with single newline
    text = re.sub(r'\n\n+', '\n', text)
    
    # Remove extra spaces (but preserve single spaces)
    text = re.sub(r' +', ' ', text)
    
    # Clean up spaces around newlines
    text = re.sub(r' +\n', '\n', text)
    text = re.sub(r'\n +', '\n', text)
    
    return text
