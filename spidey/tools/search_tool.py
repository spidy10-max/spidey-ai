"""
Spidey Search Tool
Search the internet using DuckDuckGo (No API key needed!)
Day 39 — Internet & Web Tools
"""

import requests
from datetime import datetime

try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


class SearchTool:
    """Internet search tool for Spidey AI Assistant"""

    def __init__(self):
        self.name = "search"
        self.description = "Search the internet for any query using DuckDuckGo"
        self.enabled = DDGS_AVAILABLE

    def is_available(self):
        """Check if search is available"""
        return self.enabled

    # ========================================
    # Text Search
    # ========================================

    def search(self, query, count=5, region="wt-wt"):
        """
        Search the internet for any query.

        Args:
            query: What to search for
            count: Number of results (1-10)
            region: Region code (wt-wt=worldwide, pk-en=Pakistan, us-en=US)

        Returns:
            Formatted string with search results
        """
        if not self.enabled:
            return self._fallback_search(query, count)

        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, region=region, max_results=count):
                    results.append(r)

            if not results:
                return f"🔍 No results found for '{query}'"

            return self._format_text_results(results, query)

        except Exception as e:
            print(f"   ⚠️ DDGS failed: {e}, trying fallback...")
            return self._fallback_search(query, count)

    def search_quick(self, query):
        """
        Quick search — returns just the instant answer.
        Good for facts, definitions, calculations.

        Args:
            query: Question or topic

        Returns:
            Quick answer string
        """
        if not self.enabled:
            return f"⚠️ Install duckduckgo-search: pip install duckduckgo-search"

        try:
            with DDGS() as ddgs:
                # Try instant answer first
                for r in ddgs.answers(query):
                    if r.get("text"):
                        answer = r["text"]
                        source = r.get("url", "DuckDuckGo")
                        return (
                            f"\n💡 Quick Answer: {query}\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"{answer}\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"🔗 Source: {source}"
                        )

            # No instant answer, do regular search
            return self.search(query, count=3)

        except Exception as e:
            return f"⚠️ Quick search failed: {str(e)}"

    # ========================================
    # News Search
    # ========================================

    def search_news(self, query, count=5):
        """
        Search latest news about a topic.

        Args:
            query: News topic to search
            count: Number of results

        Returns:
            Formatted news results
        """
        if not self.enabled:
            return f"⚠️ Install duckduckgo-search: pip install duckduckgo-search"

        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.news(query, max_results=count):
                    results.append(r)

            if not results:
                return f"📰 No news found for '{query}'"

            return self._format_news_results(results, query)

        except Exception as e:
            return f"⚠️ News search failed: {str(e)}"

    # ========================================
    # Image Search
    # ========================================

    def search_images(self, query, count=5):
        """
        Search for images.

        Args:
            query: What to search images for
            count: Number of results

        Returns:
            Formatted image results with URLs
        """
        if not self.enabled:
            return f"⚠️ Install duckduckgo-search: pip install duckduckgo-search"

        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.images(query, max_results=count):
                    results.append(r)

            if not results:
                return f"🖼️ No images found for '{query}'"

            return self._format_image_results(results, query)

        except Exception as e:
            return f"⚠️ Image search failed: {str(e)}"

    # ========================================
    # Video Search
    # ========================================

    def search_videos(self, query, count=5):
        """
        Search for videos (YouTube, etc.)

        Args:
            query: What to search videos for
            count: Number of results

        Returns:
            Formatted video results
        """
        if not self.enabled:
            return f"⚠️ Install duckduckgo-search: pip install duckduckgo-search"

        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.videos(query, max_results=count):
                    results.append(r)

            if not results:
                return f"🎬 No videos found for '{query}'"

            return self._format_video_results(results, query)

        except Exception as e:
            return f"⚠️ Video search failed: {str(e)}"

    # ========================================
    # Page Scraper (Get content from URL)
    # ========================================

    def get_page_summary(self, url, max_chars=1000):
        """
        Fetch and extract text content from a webpage.

        Args:
            url: Webpage URL
            max_chars: Maximum characters to return

        Returns:
            Extracted text content
        """
        if not BS4_AVAILABLE:
            return "⚠️ Install beautifulsoup4: pip install beautifulsoup4"

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36"
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove unwanted tags
            for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()

            # Get text
            text = soup.get_text(separator="\n", strip=True)

            # Clean up
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            clean_text = "\n".join(lines)

            # Truncate
            if len(clean_text) > max_chars:
                clean_text = clean_text[:max_chars] + "..."

            return (
                f"\n🌐 Page Summary: {url}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{clean_text}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )

        except requests.exceptions.Timeout:
            return "⚠️ Page load timed out."
        except requests.exceptions.RequestException as e:
            return f"⚠️ Failed to fetch page: {str(e)}"
        except Exception as e:
            return f"⚠️ Page scrape error: {str(e)}"

    # ========================================
    # Fallback Search (No library needed)
    # ========================================

    def _fallback_search(self, query, count=5):
        """
        Fallback search using DuckDuckGo HTML (no library needed).
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36"
            }

            params = {"q": query, "kl": "wt-wt"}
            response = requests.get(
                "https://html.duckduckgo.com/html/",
                params=params,
                headers=headers,
                timeout=10
            )

            if not BS4_AVAILABLE:
                return (
                    f"🔍 Search for: '{query}'\n"
                    f"🔗 https://duckduckgo.com/?q={query.replace(' ', '+')}\n\n"
                    f"⚠️ Install libraries for better results:\n"
                    f"   pip install duckduckgo-search beautifulsoup4"
                )

            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            for result in soup.select(".result")[:count]:
                title_tag = result.select_one(".result__title a")
                snippet_tag = result.select_one(".result__snippet")

                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag.get("href", "")
                    snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""

                    results.append({
                        "title": title,
                        "href": link,
                        "body": snippet
                    })

            if not results:
                return f"🔍 No results found for '{query}'"

            return self._format_text_results(results, query)

        except Exception as e:
            return f"⚠️ Fallback search failed: {str(e)}"

    # ========================================
    # Formatting Methods
    # ========================================

    def _format_text_results(self, results, query):
        """Format text search results"""
        lines = [
            f"\n🔍 Search Results — '{query}'",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            url = r.get("href", r.get("url", ""))
            snippet = r.get("body", r.get("snippet", ""))

            lines.append(f"\n  {i}. 🌐 {title}")

            if snippet:
                snip = snippet[:200] + "..." if len(snippet) > 200 else snippet
                lines.append(f"     📝 {snip}")

            if url:
                lines.append(f"     🔗 {url}")

        lines.append(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🕐 Searched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return "\n".join(lines)

    def _format_news_results(self, results, query):
        """Format news search results"""
        lines = [
            f"\n📰 News Search — '{query}'",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            source = r.get("source", "Unknown")
            url = r.get("url", "")
            date = r.get("date", "")
            body = r.get("body", "")

            lines.append(f"\n  {i}. 📌 {title}")
            lines.append(f"     📰 {source} | 📅 {date[:16] if date else 'Unknown'}")

            if body:
                snip = body[:150] + "..." if len(body) > 150 else body
                lines.append(f"     📝 {snip}")

            if url:
                lines.append(f"     🔗 {url}")

        lines.append(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🕐 Searched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return "\n".join(lines)

    def _format_image_results(self, results, query):
        """Format image search results"""
        lines = [
            f"\n🖼️ Image Search — '{query}'",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            image_url = r.get("image", "")
            source = r.get("source", "")
            size = f"{r.get('width', '?')}x{r.get('height', '?')}"

            lines.append(f"\n  {i}. 🖼️ {title}")
            lines.append(f"     📐 Size: {size}")
            lines.append(f"     🔗 {image_url}")
            if source:
                lines.append(f"     🌐 {source}")

        lines.append(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        return "\n".join(lines)

    def _format_video_results(self, results, query):
        """Format video search results"""
        lines = [
            f"\n🎬 Video Search — '{query}'",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            url = r.get("content", r.get("url", ""))
            publisher = r.get("publisher", "Unknown")
            duration = r.get("duration", "")
            views = r.get("statistics", {}).get("viewCount", "")

            lines.append(f"\n  {i}. 🎬 {title}")
            lines.append(f"     📺 {publisher}")

            if duration:
                lines.append(f"     ⏱️ Duration: {duration}")

            if views:
                lines.append(f"     👀 Views: {views}")

            if url:
                lines.append(f"     🔗 {url}")

        lines.append(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        return "\n".join(lines)


# ========================================
# Standalone Test
# ========================================
if __name__ == "__main__":
    print("🕷️ Spidey Search Tool — Testing\n")

    tool = SearchTool()

    if tool.is_available():
        print("✅ DuckDuckGo search ready!\n")
    else:
        print("⚠️ duckduckgo-search not installed, using fallback\n")

    # Test 1: Basic search
    print("=" * 50)
    print("TEST 1: Basic Search — Python programming")
    print("=" * 50)
    print(tool.search("Python programming tutorial", count=3))

    # Test 2: Quick answer
    print("\n" + "=" * 50)
    print("TEST 2: Quick Answer — What is Python")
    print("=" * 50)
    print(tool.search_quick("What is Python programming language"))

    # Test 3: News search
    print("\n" + "=" * 50)
    print("TEST 3: News Search — AI")
    print("=" * 50)
    print(tool.search_news("artificial intelligence 2025", count=3))

    # Test 4: Video search
    print("\n" + "=" * 50)
    print("TEST 4: Video Search — Python tutorial")
    print("=" * 50)
    print(tool.search_videos("Python FastAPI tutorial", count=3))

    # Test 5: Image search
    print("\n" + "=" * 50)
    print("TEST 5: Image Search — AI robot")
    print("=" * 50)
    print(tool.search_images("AI robot assistant", count=3))

    # Test 6: Page summary
    print("\n" + "=" * 50)
    print("TEST 6: Page Summary")
    print("=" * 50)
    print(tool.get_page_summary("https://en.wikipedia.org/wiki/Python_(programming_language)", max_chars=500))

    # Test 7: Pakistan related search
    print("\n" + "=" * 50)
    print("TEST 7: Pakistan Search")
    print("=" * 50)
    print(tool.search("Pakistan cricket team 2025", count=3, region="pk-en"))