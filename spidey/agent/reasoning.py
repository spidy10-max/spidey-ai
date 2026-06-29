"""
Spidey AI Reasoning Engine
AI decides which tool to use, what action, and what parameters
Day 46 — Smart reasoning for the agent
"""

import re
import json


class ReasoningEngine:
    """
    Smart reasoning engine that:
    1. Analyzes user's task
    2. Breaks it into sub-tasks
    3. Maps each sub-task to the right tool
    4. Extracts parameters from natural language
    """

    def __init__(self, brain):
        self.brain = brain

    def analyze_task(self, task):
        """
        Ask AI to analyze a task and return structured plan.

        Args:
            task: User's natural language task

        Returns:
            dict with task analysis
        """
        prompt = f"""Analyze this task and break it into steps. For each step, specify which tool to use.

AVAILABLE TOOLS:
- weather: Get weather (params: city, units)
- news: Get news headlines (params: country, category)
- search: Search internet (params: query)
- wiki: Wikipedia info (params: topic)
- ai_think: Analyze/summarize/compare (params: question)

TASK: "{task}"

Respond in this EXACT JSON format:
{{
    "task_type": "simple" or "multi_step",
    "steps": [
        {{
            "step": 1,
            "description": "What to do",
            "tool": "tool_name",
            "action": "action_type",
            "params": {{"key": "value"}}
        }}
    ],
    "final_step": "How to combine results"
}}

EXAMPLES:

Task: "Weather in Karachi"
{{
    "task_type": "simple",
    "steps": [
        {{"step": 1, "description": "Get current weather in Karachi", "tool": "weather", "action": "current", "params": {{"city": "Karachi"}}}}
    ],
    "final_step": "Show weather data directly"
}}

Task: "Compare weather in Karachi and Lahore"
{{
    "task_type": "multi_step",
    "steps": [
        {{"step": 1, "description": "Get weather in Karachi", "tool": "weather", "action": "current", "params": {{"city": "Karachi"}}}},
        {{"step": 2, "description": "Get weather in Lahore", "tool": "weather", "action": "current", "params": {{"city": "Lahore"}}}},
        {{"step": 3, "description": "Compare both cities", "tool": "ai_think", "action": "analyze", "params": {{"question": "Compare weather data of both cities and suggest which is better"}}}}
    ],
    "final_step": "Present comparison with recommendation"
}}

Task: "Tell me about Python and find tutorials"
{{
    "task_type": "multi_step",
    "steps": [
        {{"step": 1, "description": "Get Python info from Wikipedia", "tool": "wiki", "action": "summary", "params": {{"topic": "Python (programming language)"}}}},
        {{"step": 2, "description": "Search for Python tutorials", "tool": "search", "action": "text", "params": {{"query": "Python programming tutorial for beginners"}}}}
    ],
    "final_step": "Combine Wikipedia summary with tutorial links"
}}

Now analyze this task: "{task}"
Respond with ONLY valid JSON, no extra text."""

        try:
            result = self.brain.provider_manager.chat(
                messages=[
                    {"role": "system", "content": "You are a task analyzer. Respond with ONLY valid JSON. No markdown, no extra text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=800
            )

            response = result.get("content", "")
            return self._parse_json_response(response)

        except Exception as e:
            return {
                "task_type": "simple",
                "steps": [],
                "error": str(e)
            }

    def _parse_json_response(self, response):
        """Parse JSON from AI response — handles messy responses"""

        # Clean response
        response = response.strip()

        # Remove markdown code blocks
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()

        # Try direct parse
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # Try to find JSON object in response
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # Fallback — return empty
        return {
            "task_type": "unknown",
            "steps": [],
            "error": "Could not parse AI response as JSON"
        }

    def extract_entities(self, text):
        """
        Extract entities from natural language text.
        Finds cities, topics, queries, etc.

        Args:
            text: Natural language text

        Returns:
            dict with extracted entities
        """
        prompt = f"""Extract entities from this text. Return JSON only.

Text: "{text}"

Return:
{{
    "cities": ["list of city names"],
    "topics": ["list of topics/subjects"],
    "queries": ["list of search queries"],
    "categories": ["list of categories like sports, tech, etc."],
    "countries": ["list of country names or codes"],
    "actions": ["list of requested actions like compare, search, find, etc."],
    "language": "detected language (en/ur/hi)"
}}

Respond with ONLY valid JSON."""

        try:
            result = self.brain.provider_manager.chat(
                messages=[
                    {"role": "system", "content": "Extract entities. Return ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )

            response = result.get("content", "")
            return self._parse_json_response(response)

        except Exception as e:
            return {"error": str(e)}

    def should_use_agent(self, message):
        """
        Decide if a message needs the agent or simple tool/chat is enough.

        Args:
            message: User's message

        Returns:
            dict with recommendation
        """
        msg = message.lower()

        # Multi-part indicators
        multi_indicators = [
            " and ", " aur ", " or ", " ya ",
            "compare", "muqabla", "difference",
            "both", "dono", "all",
            "then ", "phir ", "after that",
            "first ", "pehle ", "step by step",
            "also ", "bhi ",
        ]

        # Count how many indicators present
        indicator_count = sum(1 for ind in multi_indicators if ind in msg)

        # Count tool keywords
        tool_keywords = {
            "weather": ["weather", "mausam", "temperature", "forecast"],
            "news": ["news", "khabar", "headlines"],
            "search": ["search", "find", "dhoondo", "google"],
            "wiki": ["wiki", "wikipedia", "tell me about"],
        }

        tools_needed = set()
        for tool, keywords in tool_keywords.items():
            for kw in keywords:
                if kw in msg:
                    tools_needed.add(tool)
                    break

        # Decision
        if indicator_count >= 2 or len(tools_needed) >= 2:
            return {
                "use_agent": True,
                "reason": f"Multi-step task detected ({indicator_count} indicators, {len(tools_needed)} tools)",
                "tools_needed": list(tools_needed),
                "complexity": "high" if indicator_count >= 3 else "medium"
            }
        elif indicator_count >= 1 and len(tools_needed) >= 1:
            return {
                "use_agent": True,
                "reason": "Multi-part task with tool usage",
                "tools_needed": list(tools_needed),
                "complexity": "medium"
            }
        elif len(tools_needed) == 1:
            return {
                "use_agent": False,
                "reason": f"Simple single-tool task ({list(tools_needed)[0]})",
                "tools_needed": list(tools_needed),
                "complexity": "low"
            }
        else:
            return {
                "use_agent": False,
                "reason": "Simple chat — no tools needed",
                "tools_needed": [],
                "complexity": "none"
            }

    def suggest_tools(self, task):
        """
        Suggest which tools to use for a task.

        Args:
            task: User's task description

        Returns:
            List of tool suggestions with confidence
        """
        msg = task.lower()
        suggestions = []

        # Weather detection
        weather_score = 0
        weather_cities = []
        weather_words = ["weather", "mausam", "temperature", "temp", "forecast",
                         "rain", "barish", "hot", "cold", "garmi", "sardi",
                         "sunrise", "sunset", "humidity"]
        for w in weather_words:
            if w in msg:
                weather_score += 10

        if weather_score > 0:
            # Try to extract city
            cities = self._extract_cities_simple(msg)
            suggestions.append({
                "tool": "weather",
                "action": "forecast" if "forecast" in msg else "current",
                "confidence": min(weather_score, 100),
                "params": {"city": cities[0]} if cities else {},
                "all_cities": cities
            })

        # News detection
        news_score = 0
        news_words = ["news", "khabar", "headlines", "breaking", "latest news"]
        for w in news_words:
            if w in msg:
                news_score += 10

        if news_score > 0:
            category = self._detect_category(msg)
            country = self._detect_country(msg)
            suggestions.append({
                "tool": "news",
                "action": "headlines",
                "confidence": min(news_score, 100),
                "params": {"country": country, "category": category}
            })

        # Search detection
        search_score = 0
        search_words = ["search", "find", "google", "look up", "dhoondo",
                        "tutorial", "how to", "best", "top", "review"]
        for w in search_words:
            if w in msg:
                search_score += 10

        if search_score > 0:
            query = self._extract_search_query_simple(msg)
            suggestions.append({
                "tool": "search",
                "action": "text",
                "confidence": min(search_score, 100),
                "params": {"query": query}
            })

        # Wiki detection
        wiki_score = 0
        wiki_words = ["wiki", "wikipedia", "who is", "what is", "define"]
        for w in wiki_words:
            if w in msg:
                wiki_score += 10

        if wiki_score > 0:
            topic = self._extract_topic_simple(msg)
            suggestions.append({
                "tool": "wiki",
                "action": "summary",
                "confidence": min(wiki_score, 100),
                "params": {"topic": topic}
            })

        # Sort by confidence
        suggestions.sort(key=lambda x: x["confidence"], reverse=True)

        return suggestions

    def _extract_cities_simple(self, msg):
        """Simple city extraction from message"""
        # Common Pakistan cities
        pakistan_cities = [
            "karachi", "lahore", "islamabad", "rawalpindi",
            "faisalabad", "multan", "peshawar", "quetta",
            "hyderabad", "sialkot", "gujranwala", "kot addu",
            "bahawalpur", "sargodha", "sukkur"
        ]

        # International cities
        world_cities = [
            "london", "new york", "dubai", "tokyo", "paris",
            "berlin", "moscow", "beijing", "delhi", "mumbai",
            "istanbul", "cairo", "sydney", "toronto", "chicago"
        ]

        all_cities = pakistan_cities + world_cities
        found = []

        for city in all_cities:
            if city in msg:
                found.append(city.title())

        return found

    def _detect_category(self, msg):
        """Detect news category from message"""
        categories = {
            "technology": ["tech", "technology", "software", "ai", "computer"],
            "sports": ["sports", "cricket", "football", "khel"],
            "business": ["business", "karobar", "economy", "market"],
            "science": ["science", "space", "research"],
            "health": ["health", "sehat", "medical", "covid"],
            "entertainment": ["entertainment", "movie", "film", "music"],
        }

        for category, keywords in categories.items():
            for kw in keywords:
                if kw in msg:
                    return category

        return None

    def _detect_country(self, msg):
        """Detect country from message"""
        countries = {
            "pk": ["pakistan", "pak"],
            "us": ["us", "usa", "america", "american"],
            "gb": ["uk", "britain", "england", "british"],
            "in": ["india", "indian", "bharat"],
            "ae": ["uae", "dubai", "emirates"],
        }

        for code, keywords in countries.items():
            for kw in keywords:
                if kw in msg:
                    return code

        return "us"

    def _extract_search_query_simple(self, msg):
        """Extract search query from message"""
        remove = [
            "search", "find", "google", "look", "up",
            "for", "me", "please", "karo", "kro",
            "dhoondo", "show", "results", "bro"
        ]

        words = msg.split()
        query_words = [w for w in words if w.strip("?,!.") not in remove and len(w) > 1]

        return " ".join(query_words).strip()

    def _extract_topic_simple(self, msg):
        """Extract topic from message"""
        remove = [
            "wiki", "wikipedia", "what", "is", "who",
            "tell", "me", "about", "the", "a", "an",
            "please", "define", "explain", "bro"
        ]

        words = msg.split()
        topic_words = [w for w in words if w.strip("?,!.") not in remove and len(w) > 1]

        topic = " ".join(topic_words).strip()
        return topic.title() if topic else ""


# ========================================
# Standalone Test
# ========================================
if __name__ == "__main__":
    print("🕷️ Reasoning Engine — Testing\n")
    print("This needs SpideyBrain to run fully.")
    print("Testing offline methods only.\n")

    class FakeBrain:
        pass

    engine = ReasoningEngine(FakeBrain())

    # Test 1: Should use agent?
    print("=" * 50)
    print("TEST 1: Should Use Agent?")
    print("=" * 50)

    messages = [
        "What is the weather in Karachi",
        "Compare weather in Karachi and Lahore",
        "Search Python tutorials and summarize",
        "Hello how are you",
        "Weather in Lahore and latest tech news",
        "Tell me about AI from Wikipedia and search for AI courses",
        "Tell me a joke",
        "Karachi ka mausam btao aur news bhi dikhao",
    ]

    for msg in messages:
        result = engine.should_use_agent(msg)
        agent = "🤖 AGENT" if result["use_agent"] else "💬 SIMPLE"
        print(f"\n  '{msg[:45]}...'")
        print(f"  → {agent} | {result['reason']}")
        if result["tools_needed"]:
            print(f"  → Tools: {', '.join(result['tools_needed'])}")

    # Test 2: Suggest tools
    print("\n" + "=" * 50)
    print("TEST 2: Tool Suggestions")
    print("=" * 50)

    tasks = [
        "Weather in Karachi and Lahore",
        "Latest Pakistan cricket news",
        "Search best Python frameworks 2025",
        "Tell me about Elon Musk",
        "Compare weather in Dubai and London then suggest travel",
    ]

    for task in tasks:
        suggestions = engine.suggest_tools(task)
        print(f"\n  '{task[:45]}...'")
        for s in suggestions:
            print(f"  → 🔧 {s['tool']} | {s['action']} | confidence: {s['confidence']}% | {s['params']}")

    # Test 3: City extraction
    print("\n" + "=" * 50)
    print("TEST 3: City Extraction")
    print("=" * 50)

    texts = [
        "weather in karachi and lahore",
        "compare islamabad and dubai temperature",
        "london ka mausam",
        "new york aur tokyo weather",
    ]

    for text in texts:
        cities = engine._extract_cities_simple(text)
        print(f"  '{text[:40]}' → Cities: {cities}")