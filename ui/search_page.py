import streamlit as st
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from core.search_agent import create_search_agent

def show_search_page(llm):
    if "search_messages" not in st.session_state:
        st.session_state.search_messages = [
            {"role": "assistant", "content": "Hi! I'm your AI search assistant. Ask me anything!"}
        ]

    for msg in st.session_state.search_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type your question..."):
        st.session_state.search_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        agent = create_search_agent(llm)
        with st.chat_message("assistant"):
            callback = StreamlitCallbackHandler(st.container())
            response = agent.run(st.session_state.search_messages, callbacks=[callback])
            st.session_state.search_messages.append({"role": "assistant", "content": response})
            st.markdown(response)