"""
Spidey Tool Registry
Central registry of ALL tools with capabilities, parameters, and examples
Day 45 — Agent knows exactly what each tool can do
"""


class ToolRegistry:

    def __init__(self):
        self.registry = {}
        self._register_all()

    def _register_all(self):

        self.registry["weather"] = {
            "name": "Weather",
            "description": "Get real-time weather data for any city in the world",
            "capabilities": [
                "Current weather (temperature, humidity, wind, clouds)",
                "3-5 day forecast",
                "Multiple cities comparison",
                "Sunrise/sunset times"
            ],
            "actions": {
                "current": {
                    "description": "Get current weather",
                    "params": {
                        "city": "(required) City name — e.g., Karachi, London, New York",
                        "units": "(optional) metric (°C) or imperial (°F) — default: metric"
                    },
                    "examples": [
                        "weather | current | city=Karachi",
                        "weather | current | city=London, units=imperial",
                    ]
                },
                "forecast": {
                    "description": "Get weather forecast",
                    "params": {
                        "city": "(required) City name",
                        "days": "(optional) Number of days 1-5 — default: 3"
                    },
                    "examples": [
                        "weather | forecast | city=Lahore",
                        "weather | forecast | city=Islamabad, days=5"
                    ]
                }
            },
            "triggers": [
                "weather", "temperature", "forecast", "rain",
                "hot", "cold", "mausam", "garmi", "sardi"
            ]
        }

        self.registry["news"] = {
            "name": "News",
            "description": "Get latest news headlines by country and category",
            "capabilities": [
                "Top headlines by country",
                "Category news (tech, sports, business, etc.)",
                "RSS feed backup (always works)",
                "Search news by keyword"
            ],
            "actions": {
                "headlines": {
                    "description": "Get top news headlines",
                    "params": {
                        "country": "(optional) Country code: us, pk, gb, in, ae — default: us",
                        "category": "(optional) general, technology, sports, business, science, health, entertainment",
                        "count": "(optional) Number of articles 1-10 — default: 5"
                    },
                    "examples": [
                        "news | headlines | country=us",
                        "news | headlines | country=pk, category=technology",
                    ]
                },
                "search": {
                    "description": "Search news by keyword",
                    "params": {
                        "query": "(required) Search term",
                        "count": "(optional) Number of results — default: 5"
                    },
                    "examples": [
                        "news | search | query=artificial intelligence",
                    ]
                },
                "rss": {
                    "description": "Get news from RSS feeds (no API key needed)",
                    "params": {
                        "topic": "(required) world, technology, science, business, sports, health, entertainment, pakistan",
                        "count": "(optional) Number of articles — default: 5"
                    },
                    "examples": [
                        "news | rss | topic=technology",
                    ]
                }
            },
            "triggers": [
                "news", "headlines", "khabar", "breaking",
                "latest news", "current events"
            ]
        }

        self.registry["search"] = {
            "name": "Search",
            "description": "Search the internet using DuckDuckGo (no API key needed)",
            "capabilities": [
                "Text search (web results)",
                "News search",
                "Image search",
                "Video search (YouTube etc.)",
                "Quick answers (facts, definitions)",
                "Page content scraping"
            ],
            "actions": {
                "text": {
                    "description": "Search the web",
                    "params": {
                        "query": "(required) Search query",
                        "count": "(optional) Number of results 1-10 — default: 5"
                    },
                    "examples": [
                        "search | text | query=Python programming tutorial",
                        "search | text | query=best laptops 2025, count=3"
                    ]
                },
                "news": {
                    "description": "Search latest news",
                    "params": {
                        "query": "(required) News topic",
                        "count": "(optional) Number of results — default: 5"
                    },
                    "examples": [
                        "search | news | query=AI artificial intelligence 2025",
                    ]
                },
                "videos": {
                    "description": "Search for videos",
                    "params": {
                        "query": "(required) Video search query",
                        "count": "(optional) Number of results — default: 5"
                    },
                    "examples": [
                        "search | videos | query=Python FastAPI tutorial",
                    ]
                },
                "images": {
                    "description": "Search for images",
                    "params": {
                        "query": "(required) Image search query",
                        "count": "(optional) Number of results — default: 5"
                    },
                    "examples": [
                        "search | images | query=AI robot",
                    ]
                }
            },
            "triggers": [
                "search", "google", "find", "look up",
                "dhoondo", "talash"
            ]
        }

        self.registry["wiki"] = {
            "name": "Wikipedia",
            "description": "Get information from Wikipedia",
            "capabilities": [
                "Article summaries (English)",
                "Article summaries (Urdu)",
                "Full articles (truncated)",
                "Article sections list",
                "Related topics",
                "Quick one-line facts",
                "Search Wikipedia articles"
            ],
            "actions": {
                "summary": {
                    "description": "Get summary of a topic",
                    "params": {
                        "topic": "(required) Topic name — use proper names",
                        "sentences": "(optional) Number of sentences 1-10 — default: 5"
                    },
                    "examples": [
                        "wiki | summary | topic=Python (programming language)",
                        "wiki | summary | topic=Pakistan, sentences=3",
                    ]
                },
                "fact": {
                    "description": "Get a one-line fact",
                    "params": {
                        "topic": "(required) Topic name"
                    },
                    "examples": [
                        "wiki | fact | topic=Earth",
                    ]
                },
                "search": {
                    "description": "Search Wikipedia for articles",
                    "params": {
                        "topic": "(required) Search query",
                        "count": "(optional) Number of results — default: 5"
                    },
                    "examples": [
                        "wiki | search | topic=artificial intelligence",
                    ]
                },
                "urdu": {
                    "description": "Get summary in Urdu",
                    "params": {
                        "topic": "(required) Topic name"
                    },
                    "examples": [
                        "wiki | urdu | topic=پاکستان"
                    ]
                }
            },
            "triggers": [
                "wikipedia", "wiki"
            ]
        }

        self.registry["ai_think"] = {
            "name": "AI Think",
            "description": "Use AI to analyze, summarize, compare, or generate text",
            "capabilities": [
                "Analyze data from other tools",
                "Summarize long content",
                "Compare information",
                "Generate suggestions",
                "Answer follow-up questions"
            ],
            "actions": {
                "analyze": {
                    "description": "Think and analyze",
                    "params": {
                        "question": "(required) What to think about"
                    },
                    "examples": [
                        "ai_think | analyze | question=Compare weather in Karachi vs Lahore",
                        "ai_think | analyze | question=Suggest activities for 35°C weather",
                    ]
                }
            },
            "triggers": []
        }

        self.registry["final_answer"] = {
            "name": "Final Answer",
            "description": "Give the final combined answer to the user",
            "capabilities": [
                "Combine all tool results into one answer",
                "Present findings clearly"
            ],
            "actions": {
                "answer": {
                    "description": "Give final answer",
                    "params": {},
                    "examples": [
                        "final_answer | Your complete answer here"
                    ]
                }
            },
            "triggers": []
        }

    def get_tool(self, name):
        return self.registry.get(name.lower())

    def get_all_tools(self):
        return self.registry

    def get_tool_names(self):
        return list(self.registry.keys())

    def get_tool_for_task(self, task_description):
        task = task_description.lower()
        scores = []

        for name, info in self.registry.items():
            if name in ["ai_think", "final_answer"]:
                continue

            score = 0
            for trigger in info.get("triggers", []):
                if trigger in task:
                    score += len(trigger) * 2

            for cap in info.get("capabilities", []):
                for word in cap.lower().split():
                    if word in task and len(word) > 3:
                        score += 1

            if score > 0:
                scores.append((name, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def get_examples_for_tool(self, tool_name):
        tool = self.registry.get(tool_name.lower())
        if not tool:
            return []

        examples = []
        for action_name, action_info in tool.get("actions", {}).items():
            for ex in action_info.get("examples", []):
                examples.append(ex)
        return examples

    def generate_agent_prompt(self):
        lines = ["AVAILABLE TOOLS AND THEIR USAGE:\n"]

        for name, info in self.registry.items():
            lines.append(f"{'='*40}")
            lines.append(f"TOOL: {name}")
            lines.append(f"Description: {info['description']}")

            for action_name, action_info in info.get("actions", {}).items():
                lines.append(f"\n  Action: {name} | {action_name}")
                lines.append(f"  What it does: {action_info['description']}")

                if action_info.get("params"):
                    lines.append(f"  Parameters:")
                    for param, desc in action_info["params"].items():
                        lines.append(f"    - {param}: {desc}")

                if action_info.get("examples"):
                    lines.append(f"  Examples:")
                    for ex in action_info["examples"][:2]:
                        lines.append(f"    → {ex}")

            lines.append("")

        return "\n".join(lines)

    def generate_short_prompt(self):
        lines = ["TOOLS:\n"]

        for name, info in self.registry.items():
            lines.append(f"  {name}: {info['description']}")
            for action_name, action_info in info.get("actions", {}).items():
                examples = action_info.get("examples", [])
                if examples:
                    lines.append(f"    → {examples[0]}")

        return "\n".join(lines)

    def display_all(self):
        lines = [
            "\n🔧 Spidey Tool Registry",
            "━" * 50
        ]

        for name, info in self.registry.items():
            status = "🤖" if name in ["ai_think", "final_answer"] else "🔧"
            lines.append(f"\n{status} {info['name']} ({name})")
            lines.append(f"   {info['description']}")

            lines.append(f"   Capabilities:")
            for cap in info.get("capabilities", []):
                lines.append(f"     • {cap}")

            lines.append(f"   Actions:")
            for action_name, action_info in info.get("actions", {}).items():
                lines.append(f"     📌 {name} | {action_name}")
                if action_info.get("examples"):
                    lines.append(f"        Example: {action_info['examples'][0]}")

        lines.append("\n" + "━" * 50)
        return "\n".join(lines)

    def display_tool(self, tool_name):
        tool = self.registry.get(tool_name.lower())
        if not tool:
            return f"⚠️ Tool '{tool_name}' not found. Available: {', '.join(self.get_tool_names())}"

        lines = [
            f"\n🔧 {tool['name']} ({tool_name})",
            "━" * 40,
            f"📝 {tool['description']}",
            "",
            "📋 Capabilities:"
        ]

        for cap in tool.get("capabilities", []):
            lines.append(f"  • {cap}")

        lines.append("\n📌 Actions:")
        for action_name, action_info in tool.get("actions", {}).items():
            lines.append(f"\n  {action_name}: {action_info['description']}")

            if action_info.get("params"):
                lines.append(f"  Parameters:")
                for param, desc in action_info["params"].items():
                    lines.append(f"    • {param}: {desc}")

            if action_info.get("examples"):
                lines.append(f"  Examples:")
                for ex in action_info["examples"]:
                    lines.append(f"    → {ex}")

        lines.append("\n" + "━" * 40)
        return "\n".join(lines)


if __name__ == "__main__":
    print("🕷️ Spidey Tool Registry — Testing\n")

    registry = ToolRegistry()

    print("=" * 50)
    print("TEST 1: All Tools")
    print("=" * 50)
    print(registry.display_all())

    print("\n" + "=" * 50)
    print("TEST 2: Weather Tool Details")
    print("=" * 50)
    print(registry.display_tool("weather"))

    print("\n" + "=" * 50)
    print("TEST 3: Tool Suggestion")
    print("=" * 50)
    tasks = [
        "What is the weather in Karachi",
        "Latest technology news",
        "Search Python tutorial",
        "Tell me about Pakistan from Wikipedia",
    ]
    for task in tasks:
        suggestions = registry.get_tool_for_task(task)
        top = suggestions[0] if suggestions else ("none", 0)
        print(f"  Task: '{task[:40]}' → Best tool: {top[0]} (score: {top[1]})")

    print("\n" + "=" * 50)
    print("TEST 4: Short Agent Prompt")
    print("=" * 50)
    print(registry.generate_short_prompt())