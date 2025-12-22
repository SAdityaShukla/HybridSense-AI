import streamlit as st
from config.llm import get_llm
from config.embeddings import get_embeddings
from ui.search_page import show_search_page
from ui.rag_page import show_rag_page
from ui.summarizer_page import show_summarizer_page

st.set_page_config(page_title="HybridSense AI", page_icon="🤖", layout="centered")
st.title("HybridSense AI")
st.caption("A Hybrid Agent & RAG-Powered Intelligent Assistant")
st.divider()
st.info(
    "🚀 **HybridSense AI** intelligently combines **RAG**, **tool-using agents**, "
    "**web intelligence**, and **website & YouTube video summarization** "
    "to deliver accurate, context-aware responses.")

groq_api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    help="Get your key at https://console.groq.com"
)

if not groq_api_key:
    st.warning("Please enter your Groq API key in the sidebar.")
    st.stop()

llm = get_llm(groq_api_key)
embeddings = get_embeddings()

task = st.sidebar.selectbox(
    "Select Task",
    ["Search Engine", "PDF Conversational ChatBot", "YouTube & Website Summarizer"]
)

if task == "Search Engine":
    st.header("🔍 AI Search Engine")
    show_search_page(llm)

elif task == "PDF Conversational ChatBot":
    st.header("📚 Chat with Your PDFs")
    show_rag_page(llm, embeddings)

else:
    st.header("📹🌐 YouTube & Website Summarizer")
    show_summarizer_page(llm)