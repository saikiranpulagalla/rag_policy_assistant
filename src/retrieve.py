"""
Retrieve relevant chunks from the vector store using semantic search.
"""


def retrieve_context(
    collection,
    query: str,
    top_k: int = 3,
    similarity_threshold: float = 0.3
) -> tuple[list[str], list[dict]]:
    """
    Retrieve top-k most relevant chunks for a query.
    
    RETRIEVAL STRATEGY:
    - top_k=3: Balance between context richness and noise
      * 1 chunk: Too narrow, might miss nuance
      * 3 chunks: Captures main idea + supporting details
      * 5+ chunks: Introduces noise and irrelevant info
    - similarity_threshold=0.3: Filter out very weak matches
      * Prevents hallucinations from unrelated chunks
      * Allows "Information not available" response when needed
    
    Args:
        collection: ChromaDB collection
        query: User's question
        top_k: Number of chunks to retrieve
        similarity_threshold: Minimum similarity score (0-1)
        
    Returns:
        Tuple of (retrieved_texts, metadata)
        Returns empty list if no relevant chunks found
    """
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    # Extract texts and metadata
    retrieved_texts = []
    metadata_list = []
    
    if results['documents'] and len(results['documents']) > 0:
        for i, doc in enumerate(results['documents'][0]):
            # ChromaDB returns distances; convert to similarity (1 - distance for cosine)
            distance = results['distances'][0][i] if results['distances'] else 0
            similarity = 1 - distance
            
            # Only include if above threshold
            if similarity >= similarity_threshold:
                retrieved_texts.append(doc)
                metadata_list.append({
                    'source': results['metadatas'][0][i]['source'],
                    'similarity': round(similarity, 3)
                })
    
    return retrieved_texts, metadata_list
