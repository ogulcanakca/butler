import asyncio
import json
import aiohttp
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("serper_search")

SERPER_API_KEY = "SERPER_API_KEY"

@mcp.tool()
async def search_web(query: str, limit: int = 5) -> Dict[str, List]:
    """
    Serper API kullanarak web araması yapar.
    
    Args:
        query: Arama sorgusu
        limit: Döndürülecek maksimum sonuç sayısı
        
    Returns:
        Arama sonuçlarını içeren bir sözlük
    """
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "q": query,
        "num": limit
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://google.serper.dev/search", 
            headers=headers, 
            json=payload
        ) as response:
            if response.status == 200:
                data = await response.json()
                organic_results = []
                if "organic" in data:
                    for result in data["organic"][:limit]:
                        organic_results.append({
                            "title": result.get("title", ""),
                            "link": result.get("link", ""),
                            "snippet": result.get("snippet", "")
                        })
                
                return {
                    "query": query,
                    "results": organic_results
                }
            else:
                return {
                    "error": f"API request failed with status {response.status}",
                    "results": []
                }

if __name__ == "__main__":
    asyncio.run(mcp.run())