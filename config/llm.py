from langchain_groq import ChatGroq

def get_llm(api_key: str):
    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.7,
        streaming=True
    )