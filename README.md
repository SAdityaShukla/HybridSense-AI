# HybridSense-AI

A powerful, modular Streamlit application that combines three AI-powered features into a single, user-friendly interface:

- **AI Search Engine** – Intelligent web search with reasoning (DuckDuckGo, Wikipedia, Arxiv)
- **PDF Conversational ChatBot** – Upload PDFs and ask questions with full context awareness (RAG)
- **YouTube & Website Summarizer** – Generate concise, insightful summaries from YouTube videos or any website

Built with **LangChain**, **Groq** (ultra-fast inference), **ChromaDB**, and **Streamlit** for a smooth, real-time experience.


### Features

- **Fast LLM Inference** via Groq (Llama 3.1 70B – blazing fast & high quality)
- **Retrieval-Augmented Generation (RAG)** for accurate PDF Q&A
- **Agent-based Search** with reasoning steps shown in real-time
- **Robust Summarization** for YouTube videos and websites
- **Clean, modular architecture** – easy to extend or modify
- **Session-aware chat history** for natural conversations
- **Streamlit-native UI** – no backend required


### Project Structure

HybridSense-AI/
├── app.py                          # Main Streamlit entry point
├── config/
│   ├── llm.py                      # Groq LLM configuration
│   └── embeddings.py               # HuggingFace embeddings setup
├── core/
│   ├── search_agent.py             # ReAct agent with web search tools
│   ├── rag_pipeline.py             # PDF processing and RAG chain
│   └── summarizer.py               # YouTube & website summarization logic
├── ui/
│   ├── search_page.py              # Search engine interface
│   ├── rag_page.py                 # PDF chatbot interface
│   └── summarizer_page.py          # URL summarizer interface
├── utils/
│   └── chat_history.py             # Session-based chat history management
├── requirements.txt                # Project dependencies
└── README.md                       # Project documentation