from langchain.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import YoutubeLoader, WebBaseLoader

def summarize_content(llm, url: str) -> str:
    prompt = PromptTemplate.from_template(
        "Provide a clear and detailed summary of the content in 250-350 words:\n\n{text}"
    )


    try:
        if "youtube.com" in url or "youtu.be" in url:
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            }
            loader = WebBaseLoader(
                url,
                header_template=headers
            )

        docs = loader.load()
        if not docs or not docs[0].page_content.strip():
            return "No content could be extracted from the URL. The page might be empty, blocked, or require JavaScript rendering."

        docs = loader.load()
        chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
        return chain.run(docs)
      
    except Exception as e:
        return f" Error while loading or summarizing the URL:\n\n{str(e)}"
