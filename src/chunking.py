"""
Split documents into chunks for embedding and retrieval.
"""


def chunk_documents(documents: dict[str, str], chunk_size: int = 400, overlap: int = 50) -> list[dict]:
    """
    Split documents into overlapping chunks.
    
    CHUNKING STRATEGY:
    - chunk_size=400 tokens: Balances context richness with retrieval precision
      * Large enough to capture complete policy sections
      * Small enough to avoid noise and stay within embedding limits
    - overlap=50 tokens: Prevents losing information at chunk boundaries
      * Ensures related concepts aren't split across chunks
      * Helps with semantic continuity
    
    Why this matters for RAG:
    - Too small chunks: Lose context, need more retrievals
    - Too large chunks: Include irrelevant info, hurt ranking
    - Overlap: Bridges concepts that span boundaries
    
    Args:
        documents: Dictionary of {filename: text}
        chunk_size: Target tokens per chunk (approximate, based on word count)
        overlap: Tokens to overlap between chunks
        
    Returns:
        List of chunk dictionaries with text and metadata
    """
    chunks = []
    
    for doc_name, text in documents.items():
        # Simple token approximation: 1 token ≈ 1.3 words
        words = text.split()
        words_per_chunk = int(chunk_size / 1.3)
        words_overlap = int(overlap / 1.3)
        
        # Create overlapping chunks
        for i in range(0, len(words), words_per_chunk - words_overlap):
            chunk_words = words[i : i + words_per_chunk]
            if len(chunk_words) > 0:
                chunk_text = ' '.join(chunk_words)
                chunks.append({
                    'text': chunk_text,
                    'source': doc_name,
                    'start_idx': i
                })
        
        # Ensure we don't miss the last chunk if it's small
        if len(words) % (words_per_chunk - words_overlap) != 0:
            last_chunk_words = words[-(words_per_chunk):]
            if last_chunk_words and ' '.join(last_chunk_words) != chunks[-1]['text']:
                chunks.append({
                    'text': ' '.join(last_chunk_words),
                    'source': doc_name,
                    'start_idx': len(words) - len(last_chunk_words)
                })
    
    return chunks
