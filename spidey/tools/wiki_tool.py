"""
Spidey Wikipedia Tool
Fetch summaries, articles, and info from Wikipedia
Day 40 — Internet & Web Tools
No API key needed!
"""

import requests
from datetime import datetime

try:
    import wikipediaapi
    WIKI_API_AVAILABLE = True
except ImportError:
    WIKI_API_AVAILABLE = False

try:
    import wikipedia
    WIKI_SIMPLE_AVAILABLE = True
except ImportError:
    WIKI_SIMPLE_AVAILABLE = False


class WikiTool:
    """Wikipedia knowledge tool for Spidey AI Assistant"""

    def __init__(self):
        self.name = "wikipedia"
        self.description = "Get summaries, articles, and facts from Wikipedia"
        self.enabled = WIKI_API_AVAILABLE or WIKI_SIMPLE_AVAILABLE

        # Initialize wikipedia-api with proper user agent
        if WIKI_API_AVAILABLE:
            self.wiki = wikipediaapi.Wikipedia(
                user_agent="SpideyAI/1.0 (Student Project)",
                language="en"
            )
            self.wiki_ur = wikipediaapi.Wikipedia(
                user_agent="SpideyAI/1.0 (Student Project)",
                language="ur"
            )
        else:
            self.wiki = None
            self.wiki_ur = None

        # If simple wikipedia library available
        if WIKI_SIMPLE_AVAILABLE:
            wikipedia.set_lang("en")

    def is_available(self):
        """Check if tool is usable"""
        return self.enabled

    # ========================================
    # Summary (Short)
    # ========================================

    def get_summary(self, topic, sentences=5):
        """
        Get a short summary of any topic.

        Args:
            topic: Topic to look up (e.g., "Python programming", "Pakistan")
            sentences: Number of sentences (1-10)

        Returns:
            Formatted summary string
        """
        # Try wikipedia-api first
        if WIKI_API_AVAILABLE:
            return self._summary_via_api(topic, sentences)

        # Fallback to simple wikipedia
        if WIKI_SIMPLE_AVAILABLE:
            return self._summary_via_simple(topic, sentences)

        return self._summary_via_rest(topic, sentences)

    def _summary_via_api(self, topic, sentences=5):
        """Get summary using wikipedia-api"""
        try:
            page = self.wiki.page(topic)

            if not page.exists():
                # Try search suggestions
                suggestions = self._search_topic(topic)
                if suggestions:
                    return (
                        f"⚠️ '{topic}' not found on Wikipedia.\n\n"
                        f"🔍 Did you mean:\n" +
                        "\n".join(f"   • {s}" for s in suggestions[:5])
                    )
                return f"⚠️ '{topic}' not found on Wikipedia."

            # Get summary text
            summary = page.summary
            if sentences:
                summary_sentences = summary.split(". ")
                summary = ". ".join(summary_sentences[:sentences])
                if not summary.endswith("."):
                    summary += "."

            return (
                f"\n📚 Wikipedia — {page.title}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{summary}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔗 {page.fullurl}\n"
                f"🕐 Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

        except Exception as e:
            return f"⚠️ Wikipedia error: {str(e)}"

    def _summary_via_simple(self, topic, sentences=5):
        """Get summary using simple wikipedia library"""
        try:
            summary = wikipedia.summary(topic, sentences=sentences)

            page = wikipedia.page(topic)
            url = page.url

            return (
                f"\n📚 Wikipedia — {page.title}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{summary}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔗 {url}\n"
                f"🕐 Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:8]
            return (
                f"⚠️ '{topic}' has multiple meanings:\n\n" +
                "\n".join(f"   {i}. {opt}" for i, opt in enumerate(options, 1)) +
                f"\n\n💡 Try a more specific term."
            )

        except wikipedia.exceptions.PageError:
            return f"⚠️ '{topic}' not found on Wikipedia."

        except Exception as e:
            return f"⚠️ Wikipedia error: {str(e)}"

    def _summary_via_rest(self, topic, sentences=5):
        """Fallback: Get summary using Wikipedia REST API (no library needed)"""
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
            headers = {"User-Agent": "SpideyAI/1.0 (Student Project)"}

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                return f"⚠️ '{topic}' not found on Wikipedia."

            response.raise_for_status()
            data = response.json()

            title = data.get("title", topic)
            summary = data.get("extract", "No summary available.")
            page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
            thumbnail = data.get("thumbnail", {}).get("source", "")

            # Truncate to sentences
            if sentences:
                sents = summary.split(". ")
                summary = ". ".join(sents[:sentences])
                if not summary.endswith("."):
                    summary += "."

            result = (
                f"\n📚 Wikipedia — {title}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{summary}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔗 {page_url}"
            )

            if thumbnail:
                result += f"\n🖼️ {thumbnail}"

            result += f"\n🕐 Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            return result

        except requests.exceptions.RequestException as e:
            return f"⚠️ Wikipedia REST API error: {str(e)}"
        except Exception as e:
            return f"⚠️ Wikipedia error: {str(e)}"

    # ========================================
    # Full Article
    # ========================================

    def get_full_article(self, topic, max_chars=3000):
        """
        Get the full article text (truncated to max_chars).

        Args:
            topic: Topic name
            max_chars: Maximum characters to return

        Returns:
            Full article text (truncated)
        """
        if WIKI_API_AVAILABLE:
            try:
                page = self.wiki.page(topic)

                if not page.exists():
                    return f"⚠️ '{topic}' not found."

                text = page.text
                if len(text) > max_chars:
                    text = text[:max_chars] + "\n\n... [Truncated]"

                return (
                    f"\n📖 Full Article — {page.title}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{text}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"📊 Total length: {len(page.text)} chars\n"
                    f"🔗 {page.fullurl}"
                )

            except Exception as e:
                return f"⚠️ Error: {str(e)}"
        else:
            return self.get_summary(topic, sentences=15)

    # ========================================
    # Sections
    # ========================================

    def get_sections(self, topic):
        """
        Get the table of contents (sections) of an article.

        Args:
            topic: Topic name

        Returns:
            List of section headings
        """
        if not WIKI_API_AVAILABLE:
            return f"⚠️ Sections need wikipedia-api: pip install wikipedia-api"

        try:
            page = self.wiki.page(topic)

            if not page.exists():
                return f"⚠️ '{topic}' not found."

            lines = [
                f"\n📑 Sections — {page.title}",
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ]

            def list_sections(sections, level=0):
                for s in sections:
                    indent = "   " * level
                    lines.append(f"  {indent}📌 {s.title}")
                    if s.sections:
                        list_sections(s.sections, level + 1)

            list_sections(page.sections)

            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append(f"📊 Total sections: {len(page.sections)}")

            return "\n".join(lines)

        except Exception as e:
            return f"⚠️ Sections error: {str(e)}"

    def get_section_content(self, topic, section_name):
        """
        Get content of a specific section.

        Args:
            topic: Article topic
            section_name: Name of the section

        Returns:
            Section content
        """
        if not WIKI_API_AVAILABLE:
            return f"⚠️ Section content needs wikipedia-api: pip install wikipedia-api"

        try:
            page = self.wiki.page(topic)

            if not page.exists():
                return f"⚠️ '{topic}' not found."

            def find_section(sections, name):
                for s in sections:
                    if s.title.lower() == name.lower():
                        return s
                    found = find_section(s.sections, name)
                    if found:
                        return found
                return None

            section = find_section(page.sections, section_name)

            if not section:
                return (
                    f"⚠️ Section '{section_name}' not found in '{topic}'.\n\n"
                    f"💡 Use get_sections('{topic}') to see available sections."
                )

            text = section.text
            if len(text) > 2000:
                text = text[:2000] + "\n\n... [Truncated]"

            return (
                f"\n📖 {page.title} — {section.title}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{text}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )

        except Exception as e:
            return f"⚠️ Section error: {str(e)}"

    # ========================================
    # Search Wikipedia
    # ========================================

    def search(self, query, count=5):
        """
        Search Wikipedia for matching articles.

        Args:
            query: Search term
            count: Number of results

        Returns:
            List of matching article titles
        """
        results = self._search_topic(query, count)

        if not results:
            return f"🔍 No Wikipedia articles found for '{query}'"

        lines = [
            f"\n🔍 Wikipedia Search — '{query}'",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ]

        for i, title in enumerate(results, 1):
            lines.append(f"  {i}. 📚 {title}")

        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"💡 Use get_summary('title') to read any article.")

        return "\n".join(lines)

    def _search_topic(self, query, count=5):
        """Internal search method"""
        if WIKI_SIMPLE_AVAILABLE:
            try:
                return wikipedia.search(query, results=count)
            except Exception:
                pass

        # Fallback to REST API search
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "opensearch",
                "search": query,
                "limit": count,
                "format": "json"
            }
            headers = {"User-Agent": "SpideyAI/1.0 (Student Project)"}
            response = requests.get(url, params=params, headers=headers, timeout=10)
            data = response.json()
            return data[1] if len(data) > 1 else []
        except Exception:
            return []

    # ========================================
    # Related Topics / Links
    # ========================================

    def get_related(self, topic, count=10):
        """
        Get related topics/links from an article.

        Args:
            topic: Topic name
            count: Number of related links

        Returns:
            List of related topics
        """
        if not WIKI_API_AVAILABLE:
            return f"⚠️ Related topics need wikipedia-api: pip install wikipedia-api"

        try:
            page = self.wiki.page(topic)

            if not page.exists():
                return f"⚠️ '{topic}' not found."

            links = list(page.links.keys())[:count]

            lines = [
                f"\n🔗 Related Topics — {page.title}",
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ]

            for i, link in enumerate(links, 1):
                lines.append(f"  {i}. 📚 {link}")

            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append(f"📊 Total links: {len(page.links)}")

            return "\n".join(lines)

        except Exception as e:
            return f"⚠️ Related topics error: {str(e)}"

    # ========================================
    # Urdu Wikipedia
    # ========================================

    def get_urdu_summary(self, topic, sentences=5):
        """
        Get summary in Urdu from Urdu Wikipedia.

        Args:
            topic: Topic name (in English or Urdu)
            sentences: Number of sentences

        Returns:
            Urdu summary
        """
        if not WIKI_API_AVAILABLE:
            return self._urdu_via_rest(topic, sentences)

        try:
            page = self.wiki_ur.page(topic)

            if not page.exists():
                return f"⚠️ '{topic}' Urdu Wikipedia pe nahi mila."

            summary = page.summary
            if sentences:
                sents = summary.split("۔")
                summary = "۔".join(sents[:sentences])
                if not summary.endswith("۔"):
                    summary += "۔"

            return (
                f"\n📚 وکیپیڈیا — {page.title}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{summary}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔗 {page.fullurl}"
            )

        except Exception as e:
            return f"⚠️ Urdu Wikipedia error: {str(e)}"

    def _urdu_via_rest(self, topic, sentences=5):
        """Fallback Urdu summary via REST API"""
        try:
            url = f"https://ur.wikipedia.org/api/rest_v1/page/summary/{topic}"
            headers = {"User-Agent": "SpideyAI/1.0 (Student Project)"}

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                return f"⚠️ '{topic}' Urdu Wikipedia pe nahi mila."

            data = response.json()
            summary = data.get("extract", "Summary nahi mili.")
            title = data.get("title", topic)
            page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")

            return (
                f"\n📚 وکیپیڈیا — {title}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{summary}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔗 {page_url}"
            )

        except Exception as e:
            return f"⚠️ Urdu REST API error: {str(e)}"

    # ========================================
    # Quick Fact (One-liner)
    # ========================================

    def quick_fact(self, topic):
        """
        Get a one-line fact about any topic.

        Args:
            topic: Topic name

        Returns:
            Single sentence fact
        """
        result = self.get_summary(topic, sentences=1)

        # If it's an error, return as is
        if result.startswith("⚠️"):
            return result

        # Extract just the summary text
        lines = result.split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith(("📚", "━", "🔗", "🕐", "🖼️")):
                return f"💡 {line}"

        return result


# ========================================
# Standalone Test
# ========================================
if __name__ == "__main__":
    print("🕷️ Spidey Wikipedia Tool — Testing\n")

    tool = WikiTool()

    if not tool.is_available():
        print("⚠️ Wikipedia libraries not installed!")
        print("   pip install wikipedia-api wikipedia")
        print("   (REST API fallback will still work)\n")

    # Test 1: Summary
    print("=" * 50)
    print("TEST 1: Summary — Python")
    print("=" * 50)
    print(tool.get_summary("Python (programming language)", sentences=3))

    # Test 2: Summary — Pakistan
    print("\n" + "=" * 50)
    print("TEST 2: Summary — Pakistan")
    print("=" * 50)
    print(tool.get_summary("Pakistan", sentences=3))

    # Test 3: Search
    print("\n" + "=" * 50)
    print("TEST 3: Search — Artificial Intelligence")
    print("=" * 50)
    print(tool.search("Artificial Intelligence", count=5))

    # Test 4: Quick fact
    print("\n" + "=" * 50)
    print("TEST 4: Quick Fact — Elon Musk")
    print("=" * 50)
    print(tool.quick_fact("Elon Musk"))

    # Test 5: Sections
    print("\n" + "=" * 50)
    print("TEST 5: Sections — Machine Learning")
    print("=" * 50)
    print(tool.get_sections("Machine learning"))

    # Test 6: Related topics
    print("\n" + "=" * 50)
    print("TEST 6: Related — Python")
    print("=" * 50)
    print(tool.get_related("Python (programming language)", count=5))

    # Test 7: Invalid topic
    print("\n" + "=" * 50)
    print("TEST 7: Invalid Topic")
    print("=" * 50)
    print(tool.get_summary("asdfxyz123456"))

    # Test 8: Urdu summary
    print("\n" + "=" * 50)
    print("TEST 8: Urdu Summary — Pakistan")
    print("=" * 50)
    print(tool.get_urdu_summary("پاکستان", sentences=3))

    # Test 9: Full article (truncated)
    print("\n" + "=" * 50)
    print("TEST 9: Full Article — AI (first 500 chars)")
    print("=" * 50)
    print(tool.get_full_article("Artificial intelligence", max_chars=500))

    # Test 10: Quick facts batch
    print("\n" + "=" * 50)
    print("TEST 10: Quick Facts Batch")
    print("=" * 50)
    topics = ["Earth", "Sun", "Moon", "Mars", "Jupiter"]
    for t in topics:
        print(tool.quick_fact(t))