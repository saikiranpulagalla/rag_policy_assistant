"""
Main entry point for the RAG policy question-answering system.
"""

import os
import sys
from dotenv import load_dotenv
from src.load_docs import load_documents
from src.chunking import chunk_documents
from src.embeddings import create_vector_store, load_vector_store
from src.qa import answer_question, compare_prompts

# Load environment variables from .env file
load_dotenv()


def initialize_rag_system(data_dir: str = './data', persist_dir: str = './chroma_db') -> object:
    """
    Initialize the RAG system: load docs, chunk, embed, and create vector store.
    
    Args:
        data_dir: Directory containing policy documents
        persist_dir: Directory to persist ChromaDB
        
    Returns:
        ChromaDB collection ready for queries
    """
    print("Loading documents...")
    documents = load_documents(data_dir)
    print(f"Loaded {len(documents)} documents")
    
    print("Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks")
    
    print("Creating vector store...")
    collection = create_vector_store(chunks, persist_dir)
    print(f"Vector store created with {len(chunks)} embeddings")
    
    return collection


def load_existing_rag_system(persist_dir: str = './chroma_db') -> object:
    """
    Load an existing RAG system from persisted vector store.
    
    Args:
        persist_dir: Directory where ChromaDB is persisted
        
    Returns:
        ChromaDB collection
    """
    if not os.path.exists(persist_dir):
        print("Vector store not found. Initializing new system...")
        return initialize_rag_system()
    
    print("Loading existing vector store...")
    collection = load_vector_store(persist_dir)
    return collection


def interactive_qa(collection):
    """
    Interactive CLI for asking questions.
    
    Args:
        collection: ChromaDB collection
    """
    print("\n" + "="*60)
    print("RAG Policy Question-Answering System")
    print("="*60)
    print("Type 'quit' to exit, 'compare' to see V1 vs V2 prompts\n")
    
    while True:
        question = input("Your question: ").strip()
        
        if question.lower() == 'quit':
            print("Goodbye!")
            break
        
        if question.lower() == 'compare':
            question = input("Enter question to compare: ").strip()
            if question:
                print("\nComparing Prompt V1 (basic) vs V2 (improved)...\n")
                comparison = compare_prompts(collection, question)
                print(f"Question: {comparison['question']}\n")
                print(f"V1 (Basic): {comparison['v1_answer']}\n")
                print(f"V2 (Improved): {comparison['v2_answer']}\n")
            continue
        
        if not question:
            continue
        
        print("\nRetrieving context and generating answer...\n")
        result = answer_question(collection, question, use_v2_prompt=True)
        
        print(f"Answer: {result['answer']}\n")
        print(f"Sources: {', '.join(result['sources'])}")
        print(f"Chunks retrieved: {result['num_chunks_retrieved']}")
        print(f"Prompt version: {result['prompt_version']}\n")


def main():
    """Main entry point."""
    # Check for Gemini API key
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set")
        print("Please set it in the .env file or as an environment variable")
        sys.exit(1)
    
    # Initialize or load RAG system
    collection = load_existing_rag_system()
    
    # Start interactive Q&A
    interactive_qa(collection)


if __name__ == "__main__":
    main()
