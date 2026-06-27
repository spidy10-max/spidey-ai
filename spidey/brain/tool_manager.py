"""
Tool Manager — Manages all tools for Spidey AI Agent
"""

from spidey.tools.weather_tool import WeatherTool


class ToolManager:
    """Registry of all available tools"""
    
    def __init__(self):
        self.tools = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register all built-in tools"""
        try:
            weather = WeatherTool()
            self.tools["weather"] = {
                "instance": weather,
                "name": weather.name,
                "description": weather.description,
                "parameters": weather.parameters
            }
            print("✅ Weather tool registered")
        except Exception as e:
            print(f"⚠️ Weather tool failed to load: {e}")
    
    def get_tool(self, name: str):
        """Get a tool by name"""
        tool_info = self.tools.get(name)
        if tool_info:
            return tool_info["instance"]
        return None
    
    def list_tools(self) -> list:
        """List all available tools with descriptions"""
        return [
            {
                "name": info["name"],
                "description": info["description"],
                "parameters": info["parameters"]
            }
            for info in self.tools.values()
        ]
    
    def get_tools_prompt(self) -> str:
        """
        Generate a description of tools for the AI system prompt.
        AI will use this to decide which tool to call.
        """
        if not self.tools:
            return "No tools available."
        
        lines = ["You have access to the following tools:\n"]
        for name, info in self.tools.items():
            lines.append(f"**{name}**: {info['description']}")
            for param, desc in info['parameters'].items():
                lines.append(f"  - {param}: {desc}")
            lines.append("")
        
        lines.append(
            "To use a tool, respond with:\n"
            "TOOL_CALL: {tool_name} | {action} | {param1=value1, param2=value2}\n"
            "Example: TOOL_CALL: weather | current | city=Karachi, units=metric"
        )
        
        return "\n".join(lines)


if __name__ == "__main__":
    tm = ToolManager()
    print("\n📋 Available Tools:")
    for tool in tm.list_tools():
        print(f"  🔧 {tool['name']}: {tool['description']}")
    
    print("\n📝 Tools Prompt for AI:")
    print(tm.get_tools_prompt())
    
    # Test using a tool
    print("\n🧪 Testing weather tool through manager:")
    weather = tm.get_tool("weather")
    if weather:
        result = weather.execute("current", {"city": "Karachi"})
        print(result)