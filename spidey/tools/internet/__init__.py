"""
🌐 Spidey Internet Tools

Contains:
- weather.py  — Live weather (OpenWeatherMap)
- search.py   — Web search (DuckDuckGo)
- wiki.py     — Wikipedia summaries
- youtube.py  — YouTube video search

All tools:
- Weather: "weather in Karachi"
- Search: "search for Python tutorial"
- News: "latest news", "news about Pakistan"
- Wikipedia: "wikipedia AI", "what is machine learning"
- YouTube: "youtube Python tutorial", "play music on youtube"
"""

from spidey.tools.internet.weather import WeatherTool
from spidey.tools.internet.search import SearchTool
from spidey.tools.internet.wiki import WikiTool
from spidey.tools.internet.youtube import YouTubeTool

__all__ = [
    "WeatherTool",
    "SearchTool",
    "WikiTool",
    "YouTubeTool"
]