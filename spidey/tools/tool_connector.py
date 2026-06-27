"""
Spidey Tool Connector v2
Smart fallback: If one tool fails, try another!
Day 44 — Fixed
"""

import re
from spidey.logger import log_event, log_error


class ToolConnector:
    """
    Central hub that connects all tools to SpideyBrain.
    Now with SMART FALLBACK — if wiki fails, tries search, etc.
    """

    def __init__(self):
        self.enabled = True
        self.tools = {}
        self._load_tools()

    def _load_tools(self):
        """Load all available tools"""

        try:
            from spidey.tools.weather_tool import WeatherTool
            tool = WeatherTool()
            self.tools["weather"] = {
                "instance": tool,
                "name": "Weather",
                "description": "Get current weather and forecast",
                "available": tool.is_available()
            }
            log_event("✅ Weather tool loaded")
        except Exception as e:
            log_error(str(e), "Loading weather tool")

        try:
            from spidey.tools.news_tool import NewsTool
            tool = NewsTool()
            self.tools["news"] = {
                "instance": tool,
                "name": "News",
                "description": "Get latest news headlines",
                "available": tool.is_available()
            }
            log_event("✅ News tool loaded")
        except Exception as e:
            log_error(str(e), "Loading news tool")

        try:
            from spidey.tools.search_tool import SearchTool
            tool = SearchTool()
            self.tools["search"] = {
                "instance": tool,
                "name": "Search",
                "description": "Search the internet",
                "available": tool.is_available()
            }
            log_event("✅ Search tool loaded")
        except Exception as e:
            log_error(str(e), "Loading search tool")

        try:
            from spidey.tools.wiki_tool import WikiTool
            tool = WikiTool()
            self.tools["wiki"] = {
                "instance": tool,
                "name": "Wikipedia",
                "description": "Get information from Wikipedia",
                "available": tool.is_available()
            }
            log_event("✅ Wiki tool loaded")
        except Exception as e:
            log_error(str(e), "Loading wiki tool")

    # ========================================
    # Intent Detection — Keywords
    # ========================================

    WEATHER_KEYWORDS = [
        "weather", "mausam", "temperature", "temp",
        "forecast", "rain", "barish", "sunny", "cloudy",
        "humidity", "wind", "garmi", "sardi", "hot", "cold",
        "sunrise", "sunset", "weather in", "ka mausam",
        "ka weather", "how hot", "how cold", "degree"
    ]

    NEWS_KEYWORDS = [
        "news", "headlines", "khabar", "khabrain",
        "latest news", "top news", "breaking",
        "aaj ki khabar", "today news", "current events",
        "sports news", "tech news", "business news",
        "science news", "health news", "entertainment news",
        "pakistan news", "world news"
    ]

    WIKI_KEYWORDS = [
        "wikipedia", "wiki",
    ]

    SEARCH_KEYWORDS = [
        "search", "google", "find", "look up", "lookup",
        "search for", "dhoondo", "talash", "search karo",
        "find me", "show me results", "internet search",
    ]

    # These should go to AI brain, NOT tools
    AI_BRAIN_KEYWORDS = [
        "tell me about", "what is", "who is", "explain",
        "define", "kya hai", "kaun hai", "batao",
        "samjhao", "how to", "why", "suggest",
        "recommend", "help me", "can you", "please",
        "create", "write", "make", "generate",
        "compare", "difference between",
        "joke", "story", "poem", "hello", "hi",
        "how are you", "good morning", "thanks",
        "thank you", "bye", "okay", "ok",
        "yes", "no", "haan", "nahi"
    ]

    # ========================================
    # Main Process Command
    # ========================================

    def process_command(self, message):
        """
        Detect intent from user message and call appropriate tool.
        With SMART FALLBACK — if tool fails, tries alternatives.
        """
        if not self.enabled:
            return None

        msg = message.lower().strip()

        if len(msg) < 3:
            return None

        # Step 1: Check direct slash commands first
        direct_result = self._check_direct_commands(msg, message)
        if direct_result:
            return direct_result

        # Step 2: Check if this should go to AI brain (not tools)
        if self._should_use_ai_brain(msg):
            return None  # Let AI brain handle it

        # Step 3: Auto-detect intent
        intent = self._detect_intent(msg)

        if intent == "weather":
            return self._handle_weather(msg, message)
        elif intent == "news":
            return self._handle_news(msg, message)
        elif intent == "search":
            return self._handle_search(msg, message)
        elif intent == "wiki":
            result = self._handle_wiki(msg, message)
            # SMART FALLBACK: If wiki fails, try search
            if result and ("not found" in result.lower() or "⚠️" in result[:5]):
                topic = self._extract_topic(msg)
                if topic:
                    search_result = self._do_search(topic)
                    if search_result and "⚠️" not in search_result[:5]:
                        return search_result
            return result

        return None  # No tool matched — AI brain handles it

    # ========================================
    # Smart AI Brain Check
    # ========================================

    def _should_use_ai_brain(self, msg):
        """
        Check if this message should go to AI brain instead of tools.
        Returns True if AI brain should handle it.
        """
        # If it starts with a direct command, don't skip
        if msg.startswith("/"):
            return False

        # Check for weather — always use tool
        for kw in self.WEATHER_KEYWORDS:
            if kw in msg:
                return False

        # Check for explicit tool keywords
        for kw in ["search", "google", "dhoondo", "news", "headlines", "wiki", "wikipedia"]:
            if kw in msg:
                return False

        # Conversational / general questions → AI brain
        conversational_patterns = [
            "tell me about", "what is", "who is",
            "explain", "define", "how to",
            "can you", "please", "help me",
            "kya hai", "kaun hai", "batao",
            "samjhao", "suggest", "recommend",
            "create", "write", "make", "generate",
            "compare", "difference",
            "life in", "culture of", "history of",
            "my ", "i am", "i want", "i need",
        ]

        for pattern in conversational_patterns:
            if pattern in msg:
                # BUT if it also has a strong tool keyword, use tool
                has_tool_keyword = False
                for kw in ["weather", "news", "search", "wiki", "wikipedia"]:
                    if kw in msg:
                        has_tool_keyword = True
                        break

                if not has_tool_keyword:
                    return True  # Let AI brain handle

        # Short messages → AI brain
        if len(msg.split()) <= 3:
            # Unless it's a clear tool command
            for kw in self.WEATHER_KEYWORDS + ["news", "search", "wiki"]:
                if kw in msg:
                    return False
            return True

        # Greetings, emotions → AI brain
        greetings = [
            "hello", "hi", "hey", "hlo", "hola",
            "good morning", "good night", "bye",
            "thanks", "thank", "ok", "okay",
            "yes", "no", "haan", "nahi",
            "how are you", "whats up", "kya hal",
            "sad", "happy", "worried", "angry",
            "joke", "story", "poem", "fun"
        ]

        for g in greetings:
            if g in msg:
                return True

        return False

    # ========================================
    # Direct Commands
    # ========================================

    def _check_direct_commands(self, msg, original):
        """Check for explicit slash commands"""

        if msg.startswith("/weather"):
            city = msg.replace("/weather", "").strip()
            if not city:
                return "⚠️ City batao! Example: /weather Karachi"
            return self._get_weather(city)

        if msg.startswith("/forecast"):
            city = msg.replace("/forecast", "").strip()
            if not city:
                return "⚠️ City batao! Example: /forecast Lahore"
            return self._get_forecast(city)

        if msg.startswith("/news"):
            topic = msg.replace("/news", "").strip()
            return self._get_news(topic)

        if msg.startswith("/search"):
            query = msg.replace("/search", "").strip()
            if not query:
                return "⚠️ Kya search karna hai? Example: /search Python tutorial"
            return self._do_search(query)

        if msg.startswith("/wiki"):
            topic = msg.replace("/wiki", "").strip()
            if not topic:
                return "⚠️ Topic batao! Example: /wiki Python"
            result = self._get_wiki(topic)
            # Fallback: If wiki fails, try search
            if result and ("not found" in result.lower()):
                search_result = self._do_search(topic)
                if search_result and "⚠️" not in search_result[:5]:
                    return f"{result}\n\n🔍 Search results instead:\n{search_result}"
            return result

        if msg.startswith("/fact"):
            topic = msg.replace("/fact", "").strip()
            if not topic:
                return "⚠️ Topic batao! Example: /fact Earth"
            return self._get_fact(topic)

        if msg in ["/tools", "/tool", "/help tools"]:
            return self._list_tools()

        return None

    # ========================================
    # Intent Detection
    # ========================================

    def _detect_intent(self, msg):
        """Detect which tool to use based on message content"""

        scores = {
            "weather": 0,
            "news": 0,
            "wiki": 0,
            "search": 0
        }

        for kw in self.WEATHER_KEYWORDS:
            if kw in msg:
                scores["weather"] += len(kw) * 2  # Weather gets higher priority

        for kw in self.NEWS_KEYWORDS:
            if kw in msg:
                scores["news"] += len(kw)

        for kw in self.WIKI_KEYWORDS:
            if kw in msg:
                scores["wiki"] += len(kw) * 2  # Only explicit wiki/wikipedia

        for kw in self.SEARCH_KEYWORDS:
            if kw in msg:
                scores["search"] += len(kw)

        max_score = max(scores.values())

        if max_score == 0:
            return None

        # Higher threshold — need stronger match
        if max_score < 4:
            return None

        best_tool = max(scores, key=scores.get)

        if best_tool in self.tools and self.tools[best_tool]["available"]:
            return best_tool

        return None

    # ========================================
    # Tool Handlers
    # ========================================

    def _handle_weather(self, msg, original):
        """Handle weather-related messages"""
        city = self._extract_city(msg)

        if not city:
            return None  # Let AI brain handle — maybe it's not really weather

        forecast_words = ["forecast", "agle din", "kal", "next days", "week", "hafta"]
        if any(w in msg for w in forecast_words):
            return self._get_forecast(city)

        return self._get_weather(city)

    def _handle_news(self, msg, original):
        """Handle news-related messages"""

        category_map = {
            "tech": "technology",
            "technology": "technology",
            "sport": "sports",
            "sports": "sports",
            "khel": "sports",
            "business": "business",
            "karobar": "business",
            "science": "science",
            "health": "health",
            "sehat": "health",
            "entertainment": "entertainment",
            "film": "entertainment",
            "movie": "entertainment"
        }

        detected_category = None
        for keyword, category in category_map.items():
            if keyword in msg:
                detected_category = category
                break

        country = "us"
        country_map = {
            "pakistan": "pk", "pak": "pk",
            "india": "in", "indian": "in",
            "us": "us", "usa": "us", "america": "us",
            "uk": "gb", "britain": "gb", "england": "gb",
            "uae": "ae", "dubai": "ae"
        }

        for keyword, code in country_map.items():
            if keyword in msg:
                country = code
                break

        return self._get_news(detected_category, country)

    def _handle_wiki(self, msg, original):
        """Handle Wikipedia-related messages — ONLY when explicitly asked"""
        topic = self._extract_topic(msg)

        if not topic:
            return None  # Let AI brain handle

        urdu_words = ["urdu", "urdu mein", "اردو"]
        if any(w in msg for w in urdu_words):
            return self._get_wiki_urdu(topic)

        return self._get_wiki(topic)

    def _handle_search(self, msg, original):
        """Handle search-related messages"""
        query = self._extract_search_query(msg)

        if not query:
            return None

        video_words = ["video", "youtube", "watch", "dekho"]
        if any(w in msg for w in video_words):
            return self._do_video_search(query)

        image_words = ["image", "photo", "picture", "tasveer", "pic"]
        if any(w in msg for w in image_words):
            return self._do_image_search(query)

        return self._do_search(query)

    # ========================================
    # Tool Execution Methods
    # ========================================

    def _get_weather(self, city):
        if "weather" not in self.tools:
            return "⚠️ Weather tool not loaded."
        try:
            tool = self.tools["weather"]["instance"]
            return tool.get_current_weather(city)
        except Exception as e:
            return f"⚠️ Weather error: {str(e)}"

    def _get_forecast(self, city, days=3):
        if "weather" not in self.tools:
            return "⚠️ Weather tool not loaded."
        try:
            tool = self.tools["weather"]["instance"]
            return tool.get_forecast(city, days=days)
        except Exception as e:
            return f"⚠️ Forecast error: {str(e)}"

    def _get_news(self, category=None, country="us"):
        if "news" not in self.tools:
            return "⚠️ News tool not loaded."
        try:
            tool = self.tools["news"]["instance"]
            if category:
                return tool.get_category_news(category, country=country, count=5)
            else:
                return tool.get_top_headlines(country=country, count=5)
        except Exception as e:
            return f"⚠️ News error: {str(e)}"

    def _do_search(self, query):
        if "search" not in self.tools:
            return "⚠️ Search tool not loaded."
        try:
            tool = self.tools["search"]["instance"]
            return tool.search(query, count=5)
        except Exception as e:
            return f"⚠️ Search error: {str(e)}"

    def _do_video_search(self, query):
        if "search" not in self.tools:
            return "⚠️ Search tool not loaded."
        try:
            tool = self.tools["search"]["instance"]
            return tool.search_videos(query, count=5)
        except Exception as e:
            return f"⚠️ Video search error: {str(e)}"

    def _do_image_search(self, query):
        if "search" not in self.tools:
            return "⚠️ Search tool not loaded."
        try:
            tool = self.tools["search"]["instance"]
            return tool.search_images(query, count=5)
        except Exception as e:
            return f"⚠️ Image search error: {str(e)}"

    def _get_wiki(self, topic):
        if "wiki" not in self.tools:
            return "⚠️ Wiki tool not loaded."
        try:
            tool = self.tools["wiki"]["instance"]
            return tool.get_summary(topic, sentences=5)
        except Exception as e:
            return f"⚠️ Wiki error: {str(e)}"

    def _get_wiki_urdu(self, topic):
        if "wiki" not in self.tools:
            return "⚠️ Wiki tool not loaded."
        try:
            tool = self.tools["wiki"]["instance"]
            return tool.get_urdu_summary(topic, sentences=5)
        except Exception as e:
            return f"⚠️ Urdu wiki error: {str(e)}"

    def _get_fact(self, topic):
        if "wiki" not in self.tools:
            return "⚠️ Wiki tool not loaded."
        try:
            tool = self.tools["wiki"]["instance"]
            return tool.quick_fact(topic)
        except Exception as e:
            return f"⚠️ Fact error: {str(e)}"

    # ========================================
    # Text Extraction Helpers
    # ========================================

    def _extract_city(self, msg):
        remove_words = [
            "weather", "mausam", "temperature", "temp",
            "forecast", "in", "of", "ka", "ki", "ke",
            "kya", "hai", "ha", "batao", "dikhao", "show",
            "what", "is", "the", "whats", "how", "hot",
            "cold", "rain", "sunny", "please", "bro",
            "me", "mujhe", "tell", "get", "check"
        ]

        words = msg.split()
        city_words = []

        for word in words:
            clean = word.strip("?,!.\"'")
            if clean and clean not in remove_words and len(clean) > 1:
                city_words.append(clean)

        city = " ".join(city_words).strip()

        if city:
            city = city.title()

        return city if city else None

    def _extract_topic(self, msg):
        remove_words = [
            "wiki", "wikipedia", "please", "bro",
            "the", "a", "an", "from"
        ]

        # Remove "wiki" or "wikipedia" from message
        cleaned = msg
        for w in ["wikipedia", "wiki"]:
            cleaned = cleaned.replace(w, "")

        words = cleaned.split()
        topic_words = []

        for word in words:
            clean = word.strip("?,!.\"'")
            if clean and clean not in remove_words and len(clean) > 1:
                topic_words.append(clean)

        topic = " ".join(topic_words).strip()

        if topic:
            topic = topic.title()

        return topic if topic else None

    def _extract_search_query(self, msg):
        remove_words = [
            "search", "google", "find", "look", "up",
            "for", "me", "please", "karo", "kro",
            "dhoondo", "talash", "show", "results",
            "internet", "bro"
        ]

        words = msg.split()
        query_words = []

        for word in words:
            clean = word.strip("?,!.\"'")
            if clean and clean not in remove_words and len(clean) > 1:
                query_words.append(clean)

        return " ".join(query_words).strip() if query_words else None

    # ========================================
    # Utility Methods
    # ========================================

    def toggle(self):
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        return f"🔧 Tools {status}"

    def is_enabled(self):
        return self.enabled

    def _list_tools(self):
        lines = [
            "\n🔧 Spidey Tools",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        for key, info in self.tools.items():
            status = "✅" if info["available"] else "❌"
            lines.append(f"  {status} {info['name']} — {info['description']}")

        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("\n📌 Direct Commands:")
        lines.append("  /weather <city>     — Get weather")
        lines.append("  /forecast <city>    — Get forecast")
        lines.append("  /news [category]    — Get news")
        lines.append("  /search <query>     — Search internet")
        lines.append("  /wiki <topic>       — Wikipedia summary")
        lines.append("  /fact <topic>       — Quick fact")
        lines.append("  /tools              — Show this list")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("\n💡 Smart Detection:")
        lines.append("  'Karachi ka weather'  → Weather tool")
        lines.append("  'latest news'         → News tool")
        lines.append("  'search Python'       → Search tool")
        lines.append("  'wiki Pakistan'       → Wikipedia")
        lines.append("  'tell me about X'     → AI Brain (smart!)")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        return "\n".join(lines)

    def get_tools_info(self):
        return {
            key: {
                "name": info["name"],
                "available": info["available"],
                "description": info["description"]
            }
            for key, info in self.tools.items()
        }