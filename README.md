# HybridSense AI

A Streamlit application that puts three distinct LLM-backed tools under one interface: a web search agent, a PDF Q&A chatbot, and a content summarizer. The backend runs on Groq's inference API with LangChain orchestrating the pipelines.

**Live demo:** https://hybridsense-ai-nbdwewq8nebdneh4vcb5kd.streamlit.app

---

## What it does

### 🔍 AI Search Engine
Takes a natural language question and runs a ReAct agent that searches across DuckDuckGo, Wikipedia, and Arxiv. The agent's reasoning steps are shown in real time as it decides which source to query and how to combine the results.

### 📚 PDF Conversational Chatbot
Upload one or more PDFs and ask questions about them. Documents are split, embedded using `all-MiniLM-L6-v2`, and stored in a local ChromaDB vector store. A history-aware retriever reformulates follow-up questions before searching the store, so the conversation stays coherent across multiple turns.

### 📹 YouTube & Website Summarizer
Paste a YouTube URL or any website link and get a 250–350 word summary. YouTube transcripts are pulled via `YoutubeLoader`; general websites go through `UnstructuredURLLoader`.

---

## Tech stack

| Layer | Library / Service |
|---|---|
| LLM | Groq — `llama-3.3-70b-versatile` |
| Orchestration | LangChain |
| Embeddings | HuggingFace — `all-MiniLM-L6-v2` |
| Vector store | ChromaDB (in-process) |
| Search tools | DuckDuckGo, Arxiv, Wikipedia |
| UI | Streamlit |

---

## Project structure

```
HybridSense-AI/
│
├── app.py                   # Entry point — page config, CSS theme, sidebar routing
│
├── config/
│   ├── llm.py               # Initialises ChatGroq with the provided API key
│   └── embeddings.py        # Loads the HuggingFace sentence-transformer
│
├── core/
│   ├── search_agent.py      # Builds the ReAct agent with three search tools
│   ├── rag_pipeline.py      # PDF loading, chunking, vector store, RAG chain
│   └── summarizer.py        # Detects URL type and runs the summarise chain
│
├── ui/
│   ├── search_page.py       # Search UI — chat history, agent callbacks
│   ├── rag_page.py          # PDF upload, session ID input, chat interface
│   └── summarizer_page.py   # URL input, spinner, styled output card
│
├── utils/
│   └── chat_history.py      # Session-keyed ChatMessageHistory store
│
├── requirements.txt
└── README.md
```

---

## Setup

**Prerequisites:** Python 3.10+, a [Groq API key](https://console.groq.com)

```bash
# Clone
git clone https://github.com/SAdityaShukla/HybridSense-AI.git
cd HybridSense-AI

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

Open `http://localhost:8501` in your browser, paste your Groq API key into the sidebar, and pick a module.

---

## How each module works

### Search agent
`core/search_agent.py` initialises three tools — `DuckDuckGoSearchRun`, `ArxivQueryRun`, `WikipediaQueryRun` — and passes them to LangChain's `ZERO_SHOT_REACT_DESCRIPTION` agent. The agent decides at runtime which tool to call based on the question, then combines the results into a final answer.

### RAG pipeline
`core/rag_pipeline.py` handles two responsibilities:

1. **Ingestion** — PDFs are loaded with `PyPDFLoader`, split into 5000-character chunks (500 overlap), and embedded into an in-memory Chroma vector store.
2. **Retrieval** — A history-aware retriever uses the chat history to rewrite the latest question into a standalone query before hitting the vector store. The retrieved chunks are passed to the QA chain via `create_stuff_documents_chain`.

Chat history is kept per session ID using `RunnableWithMessageHistory`, backed by a plain dict in `st.session_state`.

### Summarizer
`core/summarizer.py` checks whether the URL is a YouTube link and picks the appropriate loader. Content is passed directly to a `load_summarize_chain` with a custom prompt requesting a 250–350 word summary.

---

## Dependencies

```
streamlit
langchain
langchain-groq
langchain-huggingface
langchain-chroma
langchain-community
chromadb
pypdf
youtube-transcript-api
unstructured
python-dotenv
validators
```

---

## Known limitations

- The ChromaDB vector store is in-process and resets on each Streamlit rerun. Re-upload PDFs if you refresh the page.
- The search agent uses `ZERO_SHOT_REACT_DESCRIPTION`, which means it has no memory of previous search turns.
- `UnstructuredURLLoader` may fail on heavily JavaScript-rendered pages.

---

## Author

**S. Aditya Shukla** — Backend & GenAI Engineer  
[GitHub](https://github.com/SAdityaShukla) 
