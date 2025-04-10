from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.tools import tool

@tool
def health_advice_retriever(query: str) -> str:
    """Searches health advice vector database and returns relevant result."""
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = FAISS.load_local("faiss_advice", embedding_model, allow_dangerous_deserialization=True)
    docs = vectorstore.similarity_search(query, k=1)
    if docs:
        return docs[0].page_content
    return "No relevant advice found."
