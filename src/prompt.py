"""
Prompt templates for RAG answer generation.
Two versions: basic and improved with hallucination prevention.
"""


PROMPT_V1_BASIC = """You are a helpful customer service assistant. Answer the user's question based on the provided policy documents.

Policy Context:
{context}

User Question: {question}

Answer:"""


PROMPT_V2_IMPROVED = """You are a customer service assistant. Your role is to answer questions ONLY using the provided policy documents.

CRITICAL RULES:
1. Answer ONLY from the provided context
2. Do NOT make up or assume information
3. If the answer is not in the documents, respond with: "Information not available in the provided documents"
4. Be concise and direct
5. If the question is partially answered, say what you know and what's missing

Policy Context:
{context}

User Question: {question}

Answer:"""


def get_prompt_v1(context: str, question: str) -> str:
    """
    Generate prompt using basic template (V1).
    
    Why V1 is basic:
    - No explicit grounding rules
    - Relies on model's default behavior
    - More prone to hallucinations
    - Good baseline for comparison
    """
    return PROMPT_V1_BASIC.format(context=context, question=question)


def get_prompt_v2(context: str, question: str) -> str:
    """
    Generate prompt using improved template (V2).
    
    Why V2 reduces hallucinations:
    - Explicit instruction: "Answer ONLY from context"
    - Clear fallback: "Information not available..."
    - Numbered rules make expectations unambiguous
    - Prevents model from filling gaps with assumptions
    - Structured format reduces creative interpretations
    
    This is a simple but effective technique called "prompt grounding"
    """
    return PROMPT_V2_IMPROVED.format(context=context, question=question)


def format_context(retrieved_texts: list[str], metadata: list[dict]) -> str:
    """
    Format retrieved chunks into readable context for the prompt.
    
    Args:
        retrieved_texts: List of retrieved chunk texts
        metadata: List of metadata dictionaries
        
    Returns:
        Formatted context string
    """
    if not retrieved_texts:
        return "[No relevant policy documents found]"
    
    formatted_parts = []
    for i, (text, meta) in enumerate(zip(retrieved_texts, metadata), 1):
        source = meta['source'].replace('.txt', '').replace('_', ' ').title()
        similarity = meta['similarity']
        formatted_parts.append(
            f"[Source: {source} (relevance: {similarity})]\\n{text}"
        )
    
    return "\\n\\n".join(formatted_parts)
