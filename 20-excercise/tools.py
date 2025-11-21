from dotenv import load_dotenv
import re
import os
import pprint
from firecrawl import FirecrawlApp
from crewai.tools import tool #1

@tool("web_search_tool") #2
def web_search_tool(query: str):
    """
    웹 검색 도구(Firecrawl)를 사용하여 최신 뉴스를 검색하고 수집합니다.
    Args:
        query: str
            검색할 쿼리를 입력합니다.
    Returns
        웹 검색 결과를 Markdown 형식으로 반환합니다.
    """

    load_dotenv()
    cleaned_chunks = []

    try:
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            return "Error: FIRECRAWL_API_KEY is not set in environment variables."
        
        firecrawl = FirecrawlApp(api_key=api_key)

        response = firecrawl.search(
            query=query,
            limit=2,
            scrape_options={
                "formats": ["markdown"],
            },
            sources=["news"]
        )

        if response.news:
            for news_item in response.news:
                try:
                    print(news_item.metadata.title)
                    title = news_item.metadata.title
                    url = news_item.metadata.url
                    markdown = news_item.markdown
                    cleaned = re.sub(r"\\+|\n+", " ", markdown).strip() # 문자열 줄바꿈 제거
                    cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned) # 링크 제거
                    cleaned_result = {
                        "title": title,
                        "url": url,
                        "markdown": cleaned,
                    }
                    cleaned_chunks.append(cleaned_result)
                except Exception as e:
                    print(f"Error processing one result: {e}")
                    continue
        else:
            print("No results found")

    except Exception as e:
        print(f"Error in web_search_tool: {e}")
        return "Error: Failed to perform web search."
    return cleaned_chunks