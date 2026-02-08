"""
Generate embeddings and store them in ChromaDB vector store.
"""

import chromadb
import os


def create_vector_store(chunks: list[dict], persist_dir: str = './chroma_db'):
    """
    Create a ChromaDB vector store and add chunks.
    
    Why ChromaDB:
    - Lightweight, no external dependencies
    - Supports local persistence
    - Built-in embedding generation
    - Simple API for retrieval
    
    Args:
        chunks: List of chunk dictionaries from chunking.py
        persist_dir: Directory to persist the vector database
        
    Returns:
        ChromaDB collection ready for retrieval
    """
    # Create persistent client
    client = chromadb.PersistentClient(path=persist_dir)
    
    # Create or get collection
    collection = client.get_or_create_collection(
        name="policies",
        metadata={"hnsw:space": "cosine"}  # Use cosine similarity
    )
    
    # Add chunks to collection
    # ChromaDB automatically generates embeddings using default model
    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[f"chunk_{i}"],
            documents=[chunk['text']],
            metadatas=[{
                'source': chunk['source'],
                'start_idx': chunk['start_idx']
            }]
        )
    
    return collection


def load_vector_store(persist_dir: str = './chroma_db'):
    """
    Load an existing ChromaDB vector store.
    
    Args:
        persist_dir: Directory where vector database is persisted
        
    Returns:
        ChromaDB collection
    """
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_collection(name="policies")
    return collection
