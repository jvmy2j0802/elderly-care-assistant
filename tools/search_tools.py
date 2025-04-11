from tools.vector_tools import health_advice_retriever
from tools.web_scraper import scrape_latest_health_tips
from langchain_core.tools import tool

@tool
def smart_health_search(query: str) -> str:
    """Performs intelligent health search using vector DB and live web scraping."""
    if "latest" in query.lower() or "news" in query.lower():
        return scrape_latest_health_tips()
    return health_advice_retriever(query)
