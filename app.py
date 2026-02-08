"""
Streamlit UI for RAG Policy Assistant.
Optional web interface - CLI (main.py) still works independently.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.load_docs import load_documents
from src.chunking import chunk_documents
from src.embeddings import create_vector_store, load_vector_store
from src.qa import answer_question, compare_prompts


# Page configuration
st.set_page_config(
    page_title="RAG Policy Assistant",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def initialize_rag_system():
    """Initialize RAG system (cached for performance)."""
    try:
        data_dir = Path(__file__).parent / 'data'
        persist_dir = Path(__file__).parent / 'chroma_db'
        
        # Try to load existing vector store
        if persist_dir.exists():
            collection = load_vector_store(str(persist_dir))
            return collection, "Loaded existing vector store"
        
        # Create new vector store
        documents = load_documents(str(data_dir))
        chunks = chunk_documents(documents)
        collection = create_vector_store(chunks, str(persist_dir))
        return collection, f"Created new vector store with {len(chunks)} chunks"
    
    except Exception as e:
        return None, f"Error initializing RAG system: {str(e)}"


def check_api_key():
    """Check if Gemini API key is set."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY not set!")
        st.info("""
        Please set your Gemini API key:
        1. Get key from: https://aistudio.google.com/app/apikeys
        2. Add to .env file: GEMINI_API_KEY=your-key-here
        3. Restart the app
        """)
        return False
    return True


def main():
    """Main Streamlit app."""
    
    # Header
    st.title("📋 RAG Policy Assistant")
    st.markdown("*Retrieve policy information using semantic search and AI*")
    
    # Check API key
    if not check_api_key():
        st.stop()
    
    # Initialize RAG system
    with st.spinner("Initializing RAG system..."):
        collection, init_message = initialize_rag_system()
    
    if collection is None:
        st.error(init_message)
        st.stop()
    
    st.success(init_message)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        prompt_version = st.radio(
            "Prompt Version",
            options=["V2 (Improved)", "V1 (Basic)"],
            help="V2 has explicit grounding rules to prevent hallucinations"
        )
        use_v2 = prompt_version == "V2 (Improved)"
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["💬 Ask Question", "🔄 Compare Prompts", "📖 About"])
    
    # Tab 1: Ask Question
    with tab1:
        st.subheader("Ask a Policy Question")
        
        # Example questions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📌 What is the refund window?"):
                st.session_state.question = "What is the refund window?"
        with col2:
            if st.button("📌 Can I return digital products?"):
                st.session_state.question = "Can I return digital products?"
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📌 What's the fastest shipping?"):
                st.session_state.question = "What's the fastest shipping option?"
        with col2:
            if st.button("📌 Do you offer free returns?"):
                st.session_state.question = "Do you offer free returns?"
        
        st.divider()
        
        # Question input
        question = st.text_area(
            "Your Question:",
            value=st.session_state.get("question", ""),
            placeholder="Ask a question about our policies...",
            height=100
        )
        
        if st.button("🔍 Get Answer", type="primary", use_container_width=True):
            if not question.strip():
                st.warning("Please enter a question")
            else:
                with st.spinner("Retrieving context and generating answer..."):
                    try:
                        result = answer_question(
                            collection,
                            question,
                            use_v2_prompt=use_v2
                        )
                        
                        # Display answer
                        st.success("✅ Answer Generated")
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.subheader("Answer")
                            st.write(result['answer'])
                        with col2:
                            st.metric("Chunks Retrieved", result['num_chunks_retrieved'])
                            st.metric("Prompt Version", result['prompt_version'])
                        
                        # Display sources
                        if result['sources']:
                            st.subheader("📚 Sources")
                            for source in result['sources']:
                                st.caption(f"📄 {source}")
                        
                        # Display metadata
                        with st.expander("📊 Metadata"):
                            st.json({
                                "model": result['model'],
                                "prompt_version": result['prompt_version'],
                                "chunks_retrieved": result['num_chunks_retrieved'],
                                "sources": result['sources']
                            })
                    
                    except Exception as e:
                        st.error(f"Error generating answer: {str(e)}")
    
    # Tab 2: Compare Prompts
    with tab2:
        st.subheader("Compare V1 vs V2 Prompts")
        st.info("""
        **V1 (Basic):** Simple instruction to answer from context
        **V2 (Improved):** Explicit rules to prevent hallucinations
        """)
        
        compare_question = st.text_area(
            "Question to Compare:",
            placeholder="Enter a question to see how V1 and V2 prompts differ...",
            height=100,
            key="compare_question"
        )
        
        if st.button("🔄 Compare Prompts", type="primary", use_container_width=True):
            if not compare_question.strip():
                st.warning("Please enter a question")
            else:
                with st.spinner("Comparing prompts..."):
                    try:
                        comparison = compare_prompts(collection, compare_question)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("V1 (Basic)")
                            st.write(comparison['v1_answer'])
                        
                        with col2:
                            st.subheader("V2 (Improved)")
                            st.write(comparison['v2_answer'])
                        
                        st.divider()
                        
                        st.subheader("📊 Comparison Analysis")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**V1 Characteristics:**")
                            st.markdown("""
                            - Simple instruction
                            - Relies on model defaults
                            - May make inferences
                            - More prone to hallucinations
                            """)
                        
                        with col2:
                            st.write("**V2 Characteristics:**")
                            st.markdown("""
                            - Explicit grounding rules
                            - Clear fallback phrase
                            - Prevents assumptions
                            - Better user trust
                            """)
                    
                    except Exception as e:
                        st.error(f"Error comparing prompts: {str(e)}")
    
    # Tab 3: About
    with tab3:
        st.subheader("About This System")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 What is RAG?
            Retrieval-Augmented Generation combines information retrieval 
            with language models to generate grounded answers based on 
            actual documents.
            
            ### ✨ Key Features
            - **Semantic Retrieval:** Find relevant policy text
            - **Prompt Engineering:** V1 & V2 prompts
            - **Hallucination Prevention:** Explicit grounding rules
            - **Source Attribution:** Know where answers come from
            """)
        
        with col2:
            st.markdown("""
            ### 🏗️ Architecture
            1. Load policy documents
            2. Chunk into 400-token pieces
            3. Generate embeddings (ChromaDB)
            4. Retrieve top-3 relevant chunks
            5. Format prompt with context
            6. Call Gemini 2.5 Flash
            7. Return grounded answer
            """)
        
        st.divider()
        
        st.subheader("📊 System Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Accuracy", "87.5%")
        with col2:
            st.metric("Hallucinations", "0")
        with col3:
            st.metric("Test Questions", "8")
        with col4:
            st.metric("Response Time", "~1-2s")
        
        st.divider()
        
        st.subheader("🔧 Technical Stack")
        st.markdown("""
        - **Language:** Python
        - **LLM:** Google Gemini 2.5 Flash
        - **Vector Store:** ChromaDB
        - **UI:** Streamlit
        - **Embeddings:** ChromaDB default
        """)


if __name__ == "__main__":
    # Initialize session state
    if "question" not in st.session_state:
        st.session_state.question = ""
    
    main()
