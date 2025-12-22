import streamlit as st
import validators
from core.summarizer import summarize_content

def show_summarizer_page(llm):
    url = st.text_input("Enter URL (YouTube or Website)", placeholder="https://youtube.com/... or https://example.com")

    if st.button("Generate Summary", type="primary"):
        if not url.strip():
            st.error("Please enter a URL.")
        elif not validators.url(url):
            st.error("Invalid URL format.")
        else:
            with st.spinner("Fetching content and summarizing..."):
                try:
                    summary = summarize_content(llm, url)
                    st.success("Summary Complete!")
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
