"""
Spidey News Tool
Fetches latest news headlines using NewsAPI + RSS backup
Day 38 — Internet & Web Tools
"""

import os
import requests
import feedparser
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class NewsTool:
    """Fetch latest news headlines for Spidey AI Assistant"""

    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY", "")
        self.base_url = "https://newsapi.org/v2"
        self.name = "news"
        self.description = "Get latest news headlines by country, topic, or search query"
        self.enabled = bool(self.api_key)

        # RSS backup feeds (free, no API key needed)
        self.rss_feeds = {
            "world": "https://feeds.bbci.co.uk/news/world/rss.xml",
            "technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
            "science": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
            "business": "https://feeds.bbci.co.uk/news/business/rss.xml",
            "sports": "https://feeds.bbci.co.uk/news/sport/rss.xml",
            "health": "https://feeds.bbci.co.uk/news/health/rss.xml",
            "entertainment": "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
            "pakistan": "https://feeds.bbci.co.uk/urdu/rss.xml",
        }

        # Valid categories for NewsAPI
        self.valid_categories = [
            "general", "business", "technology",
            "science", "health", "sports", "entertainment"
        ]

    def is_available(self):
        """Check if tool is usable (API key or RSS)"""
        return True  # RSS always works as backup

    # ========================================
    # NewsAPI Methods
    # ========================================

    def get_top_headlines(self, country="us", category=None, count=5):
        """
        Fetch top headlines by country and category.

        Args:
            country: Country code (us, pk, gb, in, ae, etc.)
            category: general, business, technology, science, health, sports, entertainment
            count: Number of headlines (1-10)
        """
        if not self.api_key:
            return self._fallback_rss(category or "world", count)

        try:
            params = {
                "apiKey": self.api_key,
                "country": country,
                "pageSize": min(count, 10)
            }

            if category and category in self.valid_categories:
                params["category"] = category

            response = requests.get(
                f"{self.base_url}/top-headlines",
                params=params,
                timeout=10
            )

            if response.status_code == 401:
                return "⚠️ Invalid NEWS_API_KEY. Check your .env file."

            if response.status_code == 429:
                print("   ⚠️ NewsAPI limit reached, switching to RSS...")
                return self._fallback_rss(category or "world", count)

            response.raise_for_status()
            data = response.json()

            if data["totalResults"] == 0:
                return f"📰 No news found for country='{country}', category='{category}'"

            return self._format_articles(
                articles=data["articles"][:count],
                title=f"Top Headlines — {country.upper()}",
                category=category
            )

        except requests.exceptions.Timeout:
            return "⚠️ News request timed out. Internet check karo."
        except requests.exceptions.ConnectionError:
            print("   ⚠️ No internet for NewsAPI, trying RSS...")
            return self._fallback_rss(category or "world", count)
        except Exception as e:
            return f"⚠️ News error: {str(e)}"

    def search_news(self, query, count=5, language="en"):
        """
        Search news by keyword/topic.

        Args:
            query: Search term (e.g., "AI", "Pakistan cricket", "Tesla")
            count: Number of results
            language: Language code (en, ur, etc.)
        """
        if not self.api_key:
            return f"⚠️ Search requires NEWS_API_KEY. Add it to .env file.\n\nTrying RSS instead...\n{self._fallback_rss('world', count)}"

        try:
            params = {
                "apiKey": self.api_key,
                "q": query,
                "pageSize": min(count, 10),
                "language": language,
                "sortBy": "publishedAt"
            }

            response = requests.get(
                f"{self.base_url}/everything",
                params=params,
                timeout=10
            )

            if response.status_code == 426:
                return "⚠️ Free NewsAPI plan doesn't support 'everything' endpoint. Use get_top_headlines() instead."

            if response.status_code == 429:
                return "⚠️ API limit reached. Try again later."

            response.raise_for_status()
            data = response.json()

            if data["totalResults"] == 0:
                return f"📰 No news found for '{query}'"

            return self._format_articles(
                articles=data["articles"][:count],
                title=f"Search Results — '{query}'"
            )

        except requests.exceptions.RequestException as e:
            return f"⚠️ Search failed: {str(e)}"
        except Exception as e:
            return f"⚠️ Search error: {str(e)}"

    def get_category_news(self, category, country="us", count=5):
        """
        Get news by category.

        Args:
            category: business, technology, science, health, sports, entertainment
            country: Country code
            count: Number of headlines
        """
        if category not in self.valid_categories:
            available = ", ".join(self.valid_categories)
            return f"⚠️ Invalid category '{category}'. Available: {available}"

        return self.get_top_headlines(country=country, category=category, count=count)

    # ========================================
    # RSS Feed Methods (Backup — No API Key)
    # ========================================

    def get_rss_news(self, topic="world", count=5):
        """
        Fetch news from BBC RSS feeds (no API key needed).

        Args:
            topic: world, technology, science, business, sports, health, entertainment, pakistan
            count: Number of headlines
        """
        return self._fallback_rss(topic, count)

    def _fallback_rss(self, topic="world", count=5):
        """Internal RSS fallback method"""
        topic = topic.lower()

        # Map NewsAPI categories to RSS feeds
        category_map = {
            "general": "world",
            "tech": "technology",
            "sport": "sports",
        }
        topic = category_map.get(topic, topic)

        feed_url = self.rss_feeds.get(topic)
        if not feed_url:
            available = ", ".join(self.rss_feeds.keys())
            return f"⚠️ RSS topic '{topic}' not found. Available: {available}"

        try:
            feed = feedparser.parse(feed_url)

            if not feed.entries:
                return f"📰 No RSS news found for '{topic}'"

            lines = [
                f"\n📰 News — {topic.title()} (via BBC RSS)",
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ]

            for i, entry in enumerate(feed.entries[:count], 1):
                title = entry.get("title", "No title")
                link = entry.get("link", "")
                published = entry.get("published", "")

                # Clean up date
                if published:
                    try:
                        pub_date = datetime.strptime(
                            published, "%a, %d %b %Y %H:%M:%S %Z"
                        ).strftime("%d %b %Y")
                    except ValueError:
                        pub_date = published[:16]
                else:
                    pub_date = "Unknown date"

                lines.append(f"\n  {i}. 📌 {title}")
                lines.append(f"     📅 {pub_date}")
                lines.append(f"     🔗 {link}")

            lines.append("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append(f"🕐 Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            return "\n".join(lines)

        except Exception as e:
            return f"⚠️ RSS feed error: {str(e)}"

    # ========================================
    # Formatting
    # ========================================

    def _format_articles(self, articles, title="News", category=None):
        """Format news articles into readable string"""
        cat_text = f" [{category.title()}]" if category else ""

        lines = [
            f"\n📰 {title}{cat_text}",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        for i, article in enumerate(articles, 1):
            headline = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown")
            url = article.get("url", "")
            description = article.get("description", "")
            published = article.get("publishedAt", "")

            # Clean date
            if published:
                try:
                    pub_date = datetime.fromisoformat(
                        published.replace("Z", "+00:00")
                    ).strftime("%d %b %Y %I:%M %p")
                except ValueError:
                    pub_date = published[:16]
            else:
                pub_date = "Unknown"

            lines.append(f"\n  {i}. 📌 {headline}")
            lines.append(f"     📰 {source} | 📅 {pub_date}")

            if description:
                # Truncate long descriptions
                desc = description[:150] + "..." if len(description) > 150 else description
                lines.append(f"     📝 {desc}")

            lines.append(f"     🔗 {url}")

        lines.append("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🕐 Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return "\n".join(lines)

    def get_available_categories(self):
        """Return list of available categories"""
        return self.valid_categories

    def get_available_rss_topics(self):
        """Return list of available RSS topics"""
        return list(self.rss_feeds.keys())


# ========================================
# Standalone Test
# ========================================
if __name__ == "__main__":
    print("🕷️ Spidey News Tool — Testing\n")

    tool = NewsTool()

    if tool.api_key:
        print("✅ NewsAPI key found!\n")
    else:
        print("⚠️ No NewsAPI key — using RSS feeds (still works!)\n")

    # Test 1: Top headlines
    print("=" * 50)
    print("TEST 1: Top Headlines — US")
    print("=" * 50)
    print(tool.get_top_headlines(country="us", count=3))

    # Test 2: Pakistan headlines
    print("\n" + "=" * 50)
    print("TEST 2: Top Headlines — Pakistan")
    print("=" * 50)
    print(tool.get_top_headlines(country="pk", count=3))

    # Test 3: Technology news
    print("\n" + "=" * 50)
    print("TEST 3: Technology News")
    print("=" * 50)
    print(tool.get_category_news("technology", count=3))

    # Test 4: Sports news
    print("\n" + "=" * 50)
    print("TEST 4: Sports News via RSS")
    print("=" * 50)
    print(tool.get_rss_news("sports", count=3))

    # Test 5: Search news
    print("\n" + "=" * 50)
    print("TEST 5: Search — AI")
    print("=" * 50)
    if tool.api_key:
        print(tool.search_news("artificial intelligence", count=3))
    else:
        print("⚠️ Search needs API key — showing RSS instead")
        print(tool.get_rss_news("technology", count=3))

    # Test 6: World news RSS
    print("\n" + "=" * 50)
    print("TEST 6: World News via RSS (No API needed)")
    print("=" * 50)
    print(tool.get_rss_news("world", count=3))

    # Test 7: Available options
    print("\n" + "=" * 50)
    print("TEST 7: Available Options")
    print("=" * 50)
    print(f"📋 Categories: {', '.join(tool.get_available_categories())}")
    print(f"📋 RSS Topics: {', '.join(tool.get_available_rss_topics())}")