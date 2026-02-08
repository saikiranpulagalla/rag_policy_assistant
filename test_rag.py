"""
Quick test script to verify RAG system works end-to-end.
Run this to test without needing OpenAI API key.
"""

import os
import sys

# Add parent directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.load_docs import load_documents, clean_text
from src.chunking import chunk_documents
from src.retrieve import retrieve_context
from src.prompt import format_context, get_prompt_v1, get_prompt_v2


def test_document_loading():
    """Test that documents load and clean correctly."""
    print("Testing document loading...")
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    documents = load_documents(data_dir)
    assert len(documents) == 3, f"Expected 3 documents, got {len(documents)}"
    assert 'refund_policy.txt' in documents
    assert 'shipping_policy.txt' in documents
    assert 'cancellation_policy.txt' in documents
    print(f"✓ Loaded {len(documents)} documents")
    return documents


def test_chunking(documents):
    """Test that chunking works correctly."""
    print("\nTesting chunking...")
    chunks = chunk_documents(documents)
    assert len(chunks) > 0, "No chunks created"
    assert all('text' in c and 'source' in c for c in chunks), "Chunks missing required fields"
    print(f"✓ Created {len(chunks)} chunks")
    print(f"  Sample chunk: {chunks[0]['text'][:100]}...")
    return chunks


def test_text_cleaning():
    """Test text cleaning function."""
    print("\nTesting text cleaning...")
    messy_text = "Hello  \n\n\n  world   \n  test"
    clean = clean_text(messy_text)
    assert "\n\n" not in clean, "Multiple newlines not removed"
    assert "  " not in clean, "Multiple spaces not removed"
    print(f"✓ Text cleaning works")
    print(f"  Before: {repr(messy_text)}")
    print(f"  After:  {repr(clean)}")


def test_prompt_formatting():
    """Test prompt formatting."""
    print("\nTesting prompt formatting...")
    
    sample_texts = [
        "Refunds are available within 30 days of purchase.",
        "Return shipping is the customer's responsibility."
    ]
    sample_metadata = [
        {'source': 'refund_policy.txt', 'similarity': 0.95},
        {'source': 'refund_policy.txt', 'similarity': 0.87}
    ]
    
    context = format_context(sample_texts, sample_metadata)
    assert "Refund Policy" in context, "Source not formatted"
    assert "0.95" in context, "Similarity not included"
    print(f"✓ Prompt formatting works")
    print(f"  Formatted context:\n{context[:200]}...")


def test_prompt_versions():
    """Test both prompt versions."""
    print("\nTesting prompt versions...")
    
    context = "Refunds are available within 30 days."
    question = "What is the refund window?"
    
    v1 = get_prompt_v1(context, question)
    v2 = get_prompt_v2(context, question)
    
    assert "CRITICAL RULES" not in v1, "V1 should not have rules"
    assert "CRITICAL RULES" in v2, "V2 should have rules"
    assert "Information not available" in v2, "V2 should have fallback"
    
    print(f"✓ Prompt versions differ correctly")
    print(f"  V1 length: {len(v1)} chars")
    print(f"  V2 length: {len(v2)} chars")


def main():
    """Run all tests."""
    print("="*60)
    print("RAG System Component Tests")
    print("="*60)
    
    try:
        documents = test_document_loading()
        chunks = test_chunking(documents)
        test_text_cleaning()
        test_prompt_formatting()
        test_prompt_versions()
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set OpenAI API key: export OPENAI_API_KEY='your-key'")
        print("3. Run interactive Q&A: python main.py")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
