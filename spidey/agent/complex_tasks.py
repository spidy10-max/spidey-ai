"""
Spidey Complex Task Handler
Pre-built complex task patterns for better agent performance
Day 47 — Multi-step task testing
"""

import re


class ComplexTaskHandler:
    """
    Handles complex multi-step tasks by breaking them into
    pre-defined patterns before sending to ReAct agent.
    """

    def __init__(self, brain):
        self.brain = brain

    def detect_and_handle(self, task):
        """
        Check if task matches a known complex pattern.
        If yes, execute optimally. If no, return None (let agent handle).

        Args:
            task: User's task string

        Returns:
            Result string or None
        """
        msg = task.lower().strip()

        # Pattern 1: Compare weather in two cities
        result = self._check_weather_compare(msg, task)
        if result:
            return result

        # Pattern 2: Weather + suggestion
        result = self._check_weather_suggest(msg, task)
        if result:
            return result

        # Pattern 3: Wiki + Search combo
        result = self._check_wiki_search(msg, task)
        if result:
            return result

        # Pattern 4: Multi-city weather
        result = self._check_multi_city_weather(msg, task)
        if result:
            return result

        # Pattern 5: News + Summary
        result = self._check_news_summary(msg, task)
        if result:
            return result

        return None  # Not a known pattern — let ReAct agent handle

    # ========================================
    # Pattern 1: Compare Weather
    # ========================================

    def _check_weather_compare(self, msg, original):
        """
        Detect: "Compare weather in Karachi and Lahore"
        """
        compare_words = ["compare", "muqabla", "difference", "vs", "versus"]
        weather_words = ["weather", "mausam", "temperature", "temp"]

        has_compare = any(w in msg for w in compare_words)
        has_weather = any(w in msg for w in weather_words)

        if not (has_compare and has_weather):
            return None

        # Extract cities
        cities = self._extract_cities(msg)

        if len(cities) < 2:
            return None

        print(f"\n🤖 Complex Task: Compare weather in {cities[0]} vs {cities[1]}")
        print("━" * 50)

        # Get weather for both cities
        weather_tool = self._get_tool("weather")
        if not weather_tool:
            return "⚠️ Weather tool not available"

        print(f"   📍 Step 1: Getting weather for {cities[0]}...")
        weather1 = weather_tool.get_current_weather(cities[0])

        print(f"   📍 Step 2: Getting weather for {cities[1]}...")
        weather2 = weather_tool.get_current_weather(cities[1])

        # Ask AI to compare
        print(f"   📍 Step 3: AI comparing both cities...")
        compare_prompt = (
            f"Compare the weather of these two cities and tell which is better to visit today:\n\n"
            f"City 1:\n{weather1}\n\n"
            f"City 2:\n{weather2}\n\n"
            f"Give a short comparison with recommendation."
        )

        try:
            result = self.brain.provider_manager.chat(
                messages=[
                    {"role": "system", "content": "You are a helpful weather advisor. Be concise."},
                    {"role": "user", "content": compare_prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )
            comparison = result.get("content", "Could not compare")
        except Exception as e:
            comparison = f"Comparison error: {str(e)}"

        print("━" * 50)
        print("✅ Task completed in 3 steps\n")

        return (
            f"🌍 Weather Comparison: {cities[0]} vs {cities[1]}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📍 {cities[0]}:\n{weather1}\n\n"
            f"📍 {cities[1]}:\n{weather2}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 Comparison:\n{comparison}"
        )

    # ========================================
    # Pattern 2: Weather + Suggestion
    # ========================================

    def _check_weather_suggest(self, msg, original):
        """
        Detect: "Weather in Lahore and suggest what to wear/do"
        """
        weather_words = ["weather", "mausam", "temperature"]
        suggest_words = [
            "suggest", "recommend", "what to wear", "kya pehnu",
            "what to do", "activities", "plan", "advice"
        ]

        has_weather = any(w in msg for w in weather_words)
        has_suggest = any(w in msg for w in suggest_words)

        if not (has_weather and has_suggest):
            return None

        cities = self._extract_cities(msg)
        if not cities:
            return None

        city = cities[0]

        print(f"\n🤖 Complex Task: Weather + Suggestion for {city}")
        print("━" * 50)

        # Get weather
        weather_tool = self._get_tool("weather")
        if not weather_tool:
            return "⚠️ Weather tool not available"

        print(f"   📍 Step 1: Getting weather for {city}...")
        weather = weather_tool.get_current_weather(city)

        print(f"   📍 Step 2: Getting forecast...")
        forecast = weather_tool.get_forecast(city, days=2)

        # AI suggestion
        print(f"   📍 Step 3: AI generating suggestions...")
        suggest_prompt = (
            f"Based on this weather data, give practical suggestions:\n\n"
            f"Current Weather:\n{weather}\n\n"
            f"Forecast:\n{forecast}\n\n"
            f"Suggest:\n"
            f"1. What to wear\n"
            f"2. Best activities\n"
            f"3. Any precautions\n"
            f"Be concise and helpful."
        )

        try:
            result = self.brain.provider_manager.chat(
                messages=[
                    {"role": "system", "content": "You are a helpful lifestyle advisor. Be concise and practical."},
                    {"role": "user", "content": suggest_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            suggestion = result.get("content", "Could not generate suggestions")
        except Exception as e:
            suggestion = f"Suggestion error: {str(e)}"

        print("━" * 50)
        print("✅ Task completed in 3 steps\n")

        return (
            f"🌤️ Weather & Suggestions — {city}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{weather}\n\n"
            f"{forecast}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 Suggestions:\n{suggestion}"
        )

    # ========================================
    # Pattern 3: Wiki + Search
    # ========================================

    def _check_wiki_search(self, msg, original):
        """
        Detect: "Tell me about Python and search for tutorials"
        """
        wiki_words = ["about", "wiki", "wikipedia", "information"]
        search_words = ["search", "find", "tutorial", "course", "learn"]
        connector_words = ["and", "aur", "also", "bhi", "then", "phir"]

        has_wiki = any(w in msg for w in wiki_words)
        has_search = any(w in msg for w in search_words)
        has_connector = any(w in msg for w in connector_words)

        if not (has_wiki and has_search and has_connector):
            return None

        # Extract topic
        topic = self._extract_topic(msg)
        if not topic:
            return None

        print(f"\n🤖 Complex Task: Wiki + Search for '{topic}'")
        print("━" * 50)

        # Wiki
        wiki_tool = self._get_tool("wiki")
        wiki_result = ""
        if wiki_tool:
            print(f"   📍 Step 1: Getting Wikipedia summary...")
            wiki_result = wiki_tool.get_summary(topic, sentences=5)
        else:
            wiki_result = "Wikipedia tool not available"

        # Search
        search_tool = self._get_tool("search")
        search_result = ""
        if search_tool:
            search_query = f"{topic} tutorial for beginners"
            print(f"   📍 Step 2: Searching '{search_query}'...")
            search_result = search_tool.search(search_query, count=5)
        else:
            search_result = "Search tool not available"

        print("━" * 50)
        print("✅ Task completed in 2 steps\n")

        return (
            f"📚 {topic} — Info + Resources\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📖 Wikipedia:\n{wiki_result}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🔍 Tutorials & Resources:\n{search_result}"
        )

    # ========================================
    # Pattern 4: Multi-city Weather
    # ========================================

    def _check_multi_city_weather(self, msg, original):
        """
        Detect: "Weather in Karachi, Lahore, and Islamabad"
        """
        weather_words = ["weather", "mausam", "temperature"]
        has_weather = any(w in msg for w in weather_words)

        if not has_weather:
            return None

        cities = self._extract_cities(msg)
        if len(cities) < 3:
            return None

        print(f"\n🤖 Complex Task: Weather for {len(cities)} cities")
        print("━" * 50)

        weather_tool = self._get_tool("weather")
        if not weather_tool:
            return "⚠️ Weather tool not available"

        results = []
        for i, city in enumerate(cities, 1):
            print(f"   📍 Step {i}: Getting weather for {city}...")
            weather = weather_tool.get_current_weather(city)
            results.append(f"📍 {city}:\n{weather}")

        print("━" * 50)
        print(f"✅ Task completed in {len(cities)} steps\n")

        return (
            f"🌍 Weather Report — {len(cities)} Cities\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n" +
            "\n\n".join(results)
        )

    # ========================================
    # Pattern 5: News + Summary
    # ========================================

    def _check_news_summary(self, msg, original):
        """
        Detect: "Get latest news and summarize" or "AI news summary"
        """
        news_words = ["news", "headlines", "khabar"]
        summary_words = ["summary", "summarize", "summarise", "khulaasa", "brief"]

        has_news = any(w in msg for w in news_words)
        has_summary = any(w in msg for w in summary_words)

        if not (has_news and has_summary):
            return None

        # Detect category
        category = self._detect_category(msg)
        country = self._detect_country(msg)

        print(f"\n🤖 Complex Task: News + Summary")
        print("━" * 50)

        # Get news
        news_tool = self._get_tool("news")
        search_tool = self._get_tool("search")

        news_result = ""
        if news_tool:
            print(f"   📍 Step 1: Fetching news...")
            if category:
                news_result = news_tool.get_category_news(category, country=country, count=5)
            else:
                news_result = news_tool.get_top_headlines(country=country, count=5)
        elif search_tool:
            query = f"latest {category or ''} news today"
            print(f"   📍 Step 1: Searching news...")
            news_result = search_tool.search_news(query, count=5)
        else:
            return "⚠️ News and Search tools not available"

        # AI Summary
        print(f"   📍 Step 2: AI summarizing...")
        try:
            result = self.brain.provider_manager.chat(
                messages=[
                    {"role": "system", "content": "Summarize these news headlines in 3-5 bullet points. Be concise."},
                    {"role": "user", "content": f"Summarize these headlines:\n\n{news_result}"}
                ],
                temperature=0.5,
                max_tokens=400
            )
            summary = result.get("content", "Could not summarize")
        except Exception as e:
            summary = f"Summary error: {str(e)}"

        print("━" * 50)
        print("✅ Task completed in 2 steps\n")

        return (
            f"📰 News Summary\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{news_result}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 AI Summary:\n{summary}"
        )

    # ========================================
    # Helper Methods
    # ========================================

    def _get_tool(self, name):
        """Get tool instance from brain's tool connector"""
        if hasattr(self.brain, 'tools') and hasattr(self.brain.tools, 'tools'):
            tool_info = self.brain.tools.tools.get(name)
            if tool_info:
                return tool_info.get("instance")
        return None

    def _extract_cities(self, msg):
        """Extract city names from message"""
        pakistan_cities = [
            "karachi", "lahore", "islamabad", "rawalpindi",
            "faisalabad", "multan", "peshawar", "quetta",
            "hyderabad", "sialkot", "gujranwala", "kot addu",
            "bahawalpur", "sargodha", "sukkur"
        ]

        world_cities = [
            "london", "new york", "dubai", "tokyo", "paris",
            "berlin", "moscow", "beijing", "delhi", "mumbai",
            "istanbul", "cairo", "sydney", "toronto", "chicago",
            "doha", "riyadh", "jeddah", "abu dhabi", "singapore"
        ]

        all_cities = pakistan_cities + world_cities
        found = []

        for city in all_cities:
            if city in msg and city.title() not in found:
                found.append(city.title())

        return found

    def _extract_topic(self, msg):
        """Extract main topic from message"""
        remove = [
            "tell", "me", "about", "and", "search", "find",
            "tutorial", "tutorials", "course", "courses",
            "learn", "wiki", "wikipedia", "information",
            "also", "then", "for", "the", "a", "an",
            "please", "bro", "show", "get"
        ]

        words = msg.split()
        topic_words = []

        for word in words:
            clean = word.strip("?,!.\"'")
            if clean and clean not in remove and len(clean) > 1:
                topic_words.append(clean)

        topic = " ".join(topic_words[:3]).strip()
        return topic.title() if topic else None

    def _detect_category(self, msg):
        """Detect news category"""
        categories = {
            "technology": ["tech", "technology", "ai", "software", "computer"],
            "sports": ["sports", "cricket", "football", "khel"],
            "business": ["business", "karobar", "economy"],
            "science": ["science", "space", "research"],
            "health": ["health", "sehat", "medical"],
            "entertainment": ["entertainment", "movie", "film"],
        }

        for cat, keywords in categories.items():
            for kw in keywords:
                if kw in msg:
                    return cat
        return None

    def _detect_country(self, msg):
        """Detect country code"""
        countries = {
            "pk": ["pakistan", "pak"],
            "us": ["us", "usa", "america"],
            "gb": ["uk", "britain", "england"],
            "in": ["india", "bharat"],
            "ae": ["uae", "dubai"],
        }

        for code, keywords in countries.items():
            for kw in keywords:
                if kw in msg:
                    return code
        return "us"