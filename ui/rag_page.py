import streamlit as st
from core.rag_pipeline import process_pdfs, create_rag_chain

def show_rag_page(llm, embeddings):
    if "store" not in st.session_state:
        st.session_state.store = {}

    session_id = st.text_input("Session ID", value="default_session", help="Unique ID to maintain chat history")
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

    rag_chain = None
    if uploaded_files:
        with st.spinner("Processing PDFs..."):
            docs = process_pdfs(uploaded_files)
            rag_chain = create_rag_chain(llm, embeddings, docs)
        st.success(f"Loaded {len(docs)} pages. You can now ask questions!")

    if question := st.chat_input("Ask about the uploaded PDFs..."):
        if not rag_chain:
            st.warning("Please upload and process PDFs first.")
        else:
            with st.spinner("Searching documents..."):
                response = rag_chain.invoke(
                    {"input": question},
                    config={"configurable": {"session_id": session_id}}
                )
                st.markdown(f"**Answer:**\n{response['answer']}")