"""
Spidey AI — Tool Registry
Agent knows all available tools and what they do!
"""
from spidey.logger import app_logger


class ToolRegistry:
    """Registry of all tools the agent can use"""

    def __init__(self, tool_connector):
        """
        Args:
            tool_connector: ToolConnector instance
        """
        self.tc = tool_connector
        self.tools = self._build_registry()
        app_logger.info(f"ToolRegistry: {len(self.tools)} tools registered")

    def _build_registry(self):
        """Build list of all available tools with descriptions"""
        return {
            # Internet
            "weather": {
                "name": "Weather",
                "description": "Get live weather for any city",
                "usage": "weather in [city]",
                "examples": ["weather in Karachi", "weather in London", "temperature in Kot Addu"],
                "category": "internet"
            },
            "web_search": {
                "name": "Web Search",
                "description": "Search the internet for anything",
                "usage": "search for [query]",
                "examples": ["search for Python tutorial", "search for latest news"],
                "category": "internet"
            },
            "news": {
                "name": "News",
                "description": "Get latest news headlines",
                "usage": "news about [topic]",
                "examples": ["news about Pakistan", "latest news", "news about technology"],
                "category": "internet"
            },
            "wikipedia": {
                "name": "Wikipedia",
                "description": "Get Wikipedia summary of any topic",
                "usage": "wikipedia [topic]",
                "examples": ["wikipedia Python", "what is machine learning"],
                "category": "internet"
            },
            "youtube": {
                "name": "YouTube",
                "description": "Search YouTube videos",
                "usage": "youtube [query]",
                "examples": ["youtube Python tutorial", "play music on youtube"],
                "category": "internet"
            },

            # Apps
            "open_app": {
                "name": "Open App",
                "description": "Open any application",
                "usage": "open [app name]",
                "examples": ["open chrome", "open notepad", "open calculator"],
                "category": "computer"
            },
            "close_app": {
                "name": "Close App",
                "description": "Close any application",
                "usage": "close [app name]",
                "examples": ["close chrome", "close notepad"],
                "category": "computer"
            },
            "open_url": {
                "name": "Open URL",
                "description": "Open a website in browser",
                "usage": "open [website]",
                "examples": ["open youtube", "open github", "open gmail"],
                "category": "computer"
            },

            # Files
            "screenshot": {
                "name": "Screenshot",
                "description": "Take a screenshot",
                "usage": "take screenshot",
                "examples": ["take screenshot", "screenshot", "capture screen"],
                "category": "computer"
            },
            "screen_record": {
                "name": "Screen Record",
                "description": "Record screen video",
                "usage": "start/stop recording",
                "examples": ["start recording", "record for 30 seconds", "stop recording"],
                "category": "computer"
            },
            "file_search": {
                "name": "File Search",
                "description": "Search files on computer",
                "usage": "find [query] files",
                "examples": ["find python files", "show recent files", "find large files"],
                "category": "computer"
            },
            "disk_info": {
                "name": "Disk Info",
                "description": "Get disk space information",
                "usage": "disk space",
                "examples": ["disk space", "storage info", "free space"],
                "category": "computer"
            },

            # System
            "system_info": {
                "name": "System Info",
                "description": "Get computer system information",
                "usage": "system info / battery / wifi",
                "examples": ["battery", "wifi", "system info", "my ip", "what time"],
                "category": "system"
            },

            # Window
            "window_control": {
                "name": "Window Control",
                "description": "Control windows - minimize, maximize, etc",
                "usage": "minimize / maximize / switch window",
                "examples": ["minimize", "maximize", "show desktop", "switch window"],
                "category": "computer"
            },
        }

    def get_tool(self, name):
        """Get a specific tool info"""
        return self.tools.get(name)

    def get_all_tools(self):
        """Get all tools"""
        return self.tools

    def get_tools_by_category(self, category):
        """Get tools in a category"""
        return {k: v for k, v in self.tools.items() if v["category"] == category}

    def get_tool_descriptions(self):
        """Get formatted descriptions for AI prompt"""
        lines = ["Available tools:"]
        for key, tool in self.tools.items():
            lines.append(f"- {tool['name']}: {tool['description']} (usage: {tool['usage']})")
        return "\n".join(lines)

    def get_categories(self):
        """Get all categories"""
        return list(set(t["category"] for t in self.tools.values()))

    def search_tools(self, query):
        """Find tools matching a query"""
        query = query.lower()
        matches = []
        for key, tool in self.tools.items():
            if (query in tool["name"].lower() or
                query in tool["description"].lower() or
                any(query in ex.lower() for ex in tool["examples"])):
                matches.append(tool)
        return matches