# RAG Policy Assistant

A clean, production-ready Retrieval-Augmented Generation system for answering policy questions using Google Gemini 2.5 Flash.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Edit `.env`:
```
GEMINI_API_KEY=your-gemini-api-key-here
MODEL=gemini-2.5-flash
```

Get your key: https://aistudio.google.com/app/apikeys

### 3. Run

**CLI Interface:**
```bash
python main.py
```

**Web Interface (Streamlit):**
```bash
streamlit run app.py
```

## Architecture

### System Flow

```mermaid
graph TD
    A["User Question"] --> B["Embedding"]
    B --> C["Semantic Search"]
    C --> D["Retrieve Top-3 Chunks"]
    D --> E["Format Prompt"]
    E --> F["Gemini 2.5 Flash"]
    F --> G["Generate Answer"]
    G --> H["Answer with Sources"]
```

### Component Diagram

```mermaid
graph LR
    subgraph Input["Input Layer"]
        Q["User Question"]
    end
    
    subgraph Retrieval["Retrieval Layer"]
        E["Embeddings<br/>ChromaDB"]
        R["Retriever<br/>Top-3 Chunks"]
    end
    
    subgraph Processing["Processing Layer"]
        P["Prompt Engineering<br/>V1 & V2"]
        F["Gemini 2.5 Flash"]
    end
    
    subgraph Output["Output Layer"]
        A["Answer"]
        S["Sources"]
    end
    
    Q --> E
    E --> R
    R --> P
    P --> F
    F --> A
    R --> S
```

### Data Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI/UI
    participant Retriever
    participant Prompt
    participant LLM
    
    User->>CLI/UI: Ask Question
    CLI/UI->>Retriever: Embed & Search
    Retriever->>Retriever: Find Top-3 Chunks
    Retriever->>Prompt: Return Chunks
    Prompt->>Prompt: Format Context
    Prompt->>LLM: Send Prompt
    LLM->>LLM: Generate Answer
    LLM->>CLI/UI: Return Answer
    CLI/UI->>User: Display Answer + Sources
```

### Module Architecture

```mermaid
graph TB
    subgraph Core["Core Modules"]
        LD["load_docs.py<br/>Load & Clean"]
        CH["chunking.py<br/>400 tokens<br/>50 overlap"]
        EM["embeddings.py<br/>ChromaDB"]
        RT["retrieve.py<br/>Top-3 Search"]
        PR["prompt.py<br/>V1 & V2"]
        QA["qa.py<br/>Answer Gen"]
    end
    
    subgraph Data["Data"]
        PD["Policy Docs<br/>3 files"]
        VS["Vector Store<br/>ChromaDB"]
    end
    
    subgraph Interface["Interfaces"]
        CLI["CLI<br/>main.py"]
        WEB["Streamlit<br/>app.py"]
    end
    
    LD --> CH
    CH --> EM
    EM --> VS
    RT --> VS
    PD --> LD
    RT --> PR
    PR --> QA
    QA --> CLI
    QA --> WEB
```

## Key Features

- **Semantic Retrieval:** Top-3 chunks with similarity threshold
- **Prompt Engineering:** V1 (basic) & V2 (grounding rules)
- **Hallucination Prevention:** Explicit rules reduce hallucinations
- **Dual Interfaces:** CLI for development, Streamlit for demos
- **Source Attribution:** Know where answers come from

## Project Structure

```
rag_policy_assistant/
├── src/                    # Core RAG modules
│   ├── load_docs.py       # Document loading
│   ├── chunking.py        # Text chunking (400 tokens, 50 overlap)
│   ├── embeddings.py      # ChromaDB vector store
│   ├── retrieve.py        # Semantic retrieval
│   ├── prompt.py          # Prompt templates (V1 & V2)
│   └── qa.py              # Answer generation
├── data/                   # Policy documents
│   ├── refund_policy.txt
│   ├── shipping_policy.txt
│   └── cancellation_policy.txt
├── eval/                   # Evaluation results
│   └── evaluation.md
├── main.py                 # CLI interface
├── app.py                  # Streamlit web interface
├── test_rag.py             # Component tests
├── .env                    # Configuration
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Retrieval Strategy

```mermaid
graph LR
    Q["Question"] --> E["Embed"]
    E --> S["Similarity Search"]
    S --> T1["Chunk 1<br/>Score: 0.95"]
    S --> T2["Chunk 2<br/>Score: 0.87"]
    S --> T3["Chunk 3<br/>Score: 0.82"]
    T1 --> F["Filter by<br/>Threshold 0.3"]
    T2 --> F
    T3 --> F
    F --> R["Return Top-3"]
```

## Prompt Engineering

```mermaid
graph TD
    C["Retrieved Context"] --> P["Prompt Template"]
    Q["User Question"] --> P
    
    P --> V1["V1: Basic<br/>Simple instruction<br/>Prone to hallucinations"]
    P --> V2["V2: Improved<br/>Explicit grounding rules<br/>Clear fallback phrase"]
    
    V1 --> L["Gemini 2.5 Flash"]
    V2 --> L
    L --> A["Answer"]
```

## Chunking Strategy

```mermaid
graph LR
    D["Document"] --> C1["Chunk 1<br/>400 tokens"]
    D --> C2["Chunk 2<br/>400 tokens<br/>50 overlap"]
    D --> C3["Chunk 3<br/>400 tokens<br/>50 overlap"]
    
    C1 --> E["Embeddings"]
    C2 --> E
    C3 --> E
    E --> V["Vector Store"]
```

## Testing & Evaluation

```mermaid
graph TD
    T["8 Test Questions"]
    
    T --> A["Answerable<br/>4 questions"]
    T --> P["Partially Answerable<br/>2 questions"]
    T --> U["Unanswerable<br/>2 questions"]
    
    A --> R1["✅ 4/4 Correct"]
    P --> R2["✅ 2/2 Correct"]
    U --> R3["⚠️ 1/2 Correct"]
    
    R1 --> ACC["87.5% Accuracy<br/>0 Hallucinations"]
    R2 --> ACC
    R3 --> ACC
```

## Interfaces

### CLI vs Streamlit

```mermaid
graph TB
    RAG["RAG Backend<br/>Shared"]
    
    RAG --> CLI["CLI Interface<br/>main.py"]
    RAG --> WEB["Streamlit UI<br/>app.py"]
    
    CLI --> C1["Command-line"]
    CLI --> C2["Lightweight"]
    CLI --> C3["No browser"]
    
    WEB --> W1["Web browser"]
    WEB --> W2["Beautiful UI"]
    WEB --> W3["Quick buttons"]
```

### Streamlit Tabs

```mermaid
graph LR
    APP["RAG Policy Assistant"]
    
    APP --> T1["💬 Ask Question"]
    APP --> T2["🔄 Compare Prompts"]
    APP --> T3["📖 About"]
    
    T1 --> T1A["Quick buttons"]
    T1 --> T1B["Text input"]
    T1 --> T1C["Answer + Sources"]
    
    T2 --> T2A["V1 Answer"]
    T2 --> T2B["V2 Answer"]
    T2 --> T2C["Comparison"]
    
    T3 --> T3A["What is RAG?"]
    T3 --> T3B["Statistics"]
    T3 --> T3C["Tech Stack"]
```

## Testing

```bash
# Run component tests (no API key needed)
python test_rag.py
```

## Technical Stack

- **Language:** Python
- **LLM:** Google Gemini 2.5 Flash
- **Vector Store:** ChromaDB
- **UI:** Streamlit (optional)
- **Config:** python-dotenv

## Performance

- **Accuracy:** 87.5% on test set
- **Hallucinations:** 0
- **Response Time:** ~1-2 seconds
- **Memory:** ~300-500MB

## Evaluation

8 test questions across answerable, partially answerable, and unanswerable categories.

See `eval/evaluation.md` for detailed results.

## Security

- API key stored in `.env` (not in code)
- `.gitignore` protects `.env`
- No hardcoded secrets
- Safe for sharing

## Example Usage

### CLI
```
Your question: What is the refund window?

Answer: You can request a refund within 30 days of purchase for most items.

Sources: refund_policy.txt
Chunks retrieved: 3
Prompt version: V2
```

### Streamlit
1. Open browser at `http://localhost:8501`
2. Click quick buttons or enter custom question
3. See answer with sources
4. Compare V1 vs V2 prompts
5. View system statistics

## Troubleshooting

**"GEMINI_API_KEY not set"**
- Check `.env` file has your key
- Restart the app

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Port 8501 already in use"**
```bash
streamlit run app.py --server.port 8502
```

## FAQ

**Q: Can I use both CLI and Streamlit?**
A: Yes! They share the same backend and vector store.

**Q: How do I add more policy documents?**
A: Add `.txt` files to `data/` and reinitialize the system.

**Q: Can I use a different LLM?**
A: Yes, modify `src/qa.py` to use Claude, Llama, or any other model.

**Q: Is this production-ready?**
A: Yes, with proper error handling and configuration management.

## Next Steps

1. Get Gemini API key
2. Edit `.env` file
3. Run `pip install -r requirements.txt`
4. Choose interface: `python main.py` or `streamlit run app.py`

## Support

- Gemini Docs: https://ai.google.dev/docs
- Streamlit Docs: https://docs.streamlit.io/
- FAQ: See `FAQ.md`

