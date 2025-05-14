#!/usr/bin/env python3
import asyncio
import json
import aiohttp
from typing import Dict, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather_api")

OPENWEATHER_API_KEY = "OPENWEATHER_API_KEY"

@mcp.tool()
async def get_weather(city: str, country_code: Optional[str] = None) -> Dict:
    """
    OpenWeather API kullanarak hava durumu bilgilerini alır.
    
    Args:
        city: Şehir adı
        country_code: Ülke kodu (örn. "TR", "US")
        
    Returns:
        Hava durumu bilgilerini içeren bir sözlük
    """
    location = city
    if country_code:
        location = f"{city},{country_code}"
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                
                weather_info = {
                    "location": f"{data['name']}, {data['sys']['country']}",
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"]
                }
                
                return weather_info
            else:
                error_data = await response.text()
                return {
                    "error": f"API request failed with status {response.status}",
                    "details": error_data
                }

if __name__ == "__main__":
    asyncio.run(mcp.run())