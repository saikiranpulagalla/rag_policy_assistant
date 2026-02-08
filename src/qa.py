"""
Question-answering pipeline: retrieve context and generate answers using Gemini.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from .retrieve import retrieve_context
from .prompt import get_prompt_v1, get_prompt_v2, format_context

# Load environment variables from .env file
load_dotenv()


def answer_question(
    collection,
    question: str,
    use_v2_prompt: bool = True,
    model: str = None
) -> dict:
    """
    Answer a question using RAG pipeline with Gemini.
    
    Pipeline:
    1. Retrieve relevant chunks from vector store
    2. Format context for LLM
    3. Generate answer using prompt template
    4. Return answer with metadata
    
    Args:
        collection: ChromaDB collection
        question: User's question
        use_v2_prompt: Use improved prompt (V2) if True, else basic (V1)
        model: Gemini model to use (defaults to env var or gemini-2.5-flash)
        
    Returns:
        Dictionary with answer, sources, and metadata
    """
    # Get API key and model from environment
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set. Please set it in .env file.")
    
    if model is None:
        model = os.getenv("MODEL", "gemini-2.5-flash")
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Step 1: Retrieve relevant context
    retrieved_texts, metadata = retrieve_context(collection, question)
    
    # Step 2: Format context
    context = format_context(retrieved_texts, metadata)
    
    # Step 3: Select prompt version
    if use_v2_prompt:
        prompt = get_prompt_v2(context, question)
    else:
        prompt = get_prompt_v1(context, question)
    
    # Step 4: Call Gemini LLM
    gemini_model = genai.GenerativeModel(model)
    response = gemini_model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,  # Low temperature for factual consistency
            max_output_tokens=500
        )
    )
    
    answer = response.text.strip()
    
    # Step 5: Return structured result
    return {
        'question': question,
        'answer': answer,
        'sources': [meta['source'] for meta in metadata],
        'num_chunks_retrieved': len(retrieved_texts),
        'prompt_version': 'V2' if use_v2_prompt else 'V1',
        'model': model
    }


def compare_prompts(collection, question: str, model: str = None) -> dict:
    """
    Compare answers from V1 and V2 prompts for evaluation.
    
    Useful for demonstrating prompt iteration and hallucination prevention.
    
    Args:
        collection: ChromaDB collection
        question: User's question
        model: Gemini model to use
        
    Returns:
        Dictionary with both V1 and V2 answers
    """
    answer_v1 = answer_question(collection, question, use_v2_prompt=False, model=model)
    answer_v2 = answer_question(collection, question, use_v2_prompt=True, model=model)
    
    return {
        'question': question,
        'v1_answer': answer_v1['answer'],
        'v2_answer': answer_v2['answer'],
        'v1_prompt': 'basic',
        'v2_prompt': 'improved with grounding rules'
    }
