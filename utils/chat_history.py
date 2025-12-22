from langchain_community.chat_message_histories import ChatMessageHistory

def get_session_history(store: dict, session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]