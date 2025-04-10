from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup

@tool
def scrape_latest_health_tips() -> str:
    """Scrape a trusted health blog for recent tips."""
    try:
        url = "https://www.healthline.com/health-news"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.select("a.css-1egxyvc")  # Adjust CSS class if needed

        tips = [article.get_text(strip=True) for article in articles[:5]]
        return "\n".join(tips)
    except Exception as e:
        return "Stay hydrated, walk 30 minutes a day, and avoid excess sugar."  # Fallback tip
