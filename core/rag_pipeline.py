import os
import streamlit as st  # Only here because session_state is Streamlit-specific
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from utils.chat_history import get_session_history

def process_pdfs(uploaded_files):
    documents = []
    for uploaded_file in uploaded_files:
        temp_path = f"./temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        loader = PyPDFLoader(temp_path)
        documents.extend(loader.load())
        os.remove(temp_path)
    return documents

def create_rag_chain(llm, embeddings, documents):
    if not documents:
        return None

    splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    splits = splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # Contextualize question
    contextualize_prompt = ChatPromptTemplate.from_messages([
        ("system", "Given a chat history and the latest user question, reformulate it into a standalone question if needed."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_prompt)

    # QA prompt
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer concisely using only the provided context. If you don't know, say so.\n\n{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    qa_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    return RunnableWithMessageHistory(
        rag_chain,
        lambda session_id: get_session_history(st.session_state.store, session_id),
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )