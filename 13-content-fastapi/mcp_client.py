from crewai.tools import tool
from crewai_tools import MCPServerAdapter
import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_MCP_PARAMS = {
    "url": f"https://mcp.firecrawl.dev/{os.getenv('FIRECRAWL_API_KEY')}/v2/mcp",
    "transport": "streamable-http",
}


@tool("firecrawl_news_search")
def firecrawl_news_search(query: str, limit: int = 3):
    """
    Firecrawl MCP의 firecrawl_search를 호출해서 'news' 소스에서 검색 결과를 가져옵니다.
    """
    with MCPServerAdapter(FIRECRAWL_MCP_PARAMS) as mcp_tools:
        search_tool = mcp_tools["firecrawl_search"]
        result = search_tool.run(
            query=query,                         # ✅ 키워드 인자로 전달
            limit=limit,
            sources=[{"type": "news"}],          # 필요하면 'web' 등으로 변경
        )
        
    return result

@tool("firecrawl_web_search")
def firecrawl_web_search(query: str, limit: int = 3):
    """
    Firecrawl MCP의 firecrawl_search를 호출해서 'web' 소스에서 검색 결과를 가져옵니다.
    """
    with MCPServerAdapter(FIRECRAWL_MCP_PARAMS) as mcp_tools:
        search_tool = mcp_tools["firecrawl_search"]
        result = search_tool.run(
            query=query,                         # ✅ 키워드 인자로 전달
            limit=limit,
            sources=[{"type": "web"}],          # 필요하면 'web' 등으로 변경
        )

    return result