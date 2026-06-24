"""
Spidey AI — Wikipedia Tool
Get summaries from Wikipedia — FREE!
"""
from spidey.logger import app_logger, log_event, log_error

try:
    import wikipediaapi
    WIKI_AVAILABLE = True
except ImportError:
    WIKI_AVAILABLE = False


class WikiTool:
    """Wikipedia summaries"""

    def __init__(self):
        if WIKI_AVAILABLE:
            self.wiki = wikipediaapi.Wikipedia(
                user_agent="SpideyAI/1.0 (spidey@example.com)",
                language="en"
            )
            app_logger.info("WikiTool ready")
        else:
            self.wiki = None
            app_logger.warning("WikiTool: wikipedia-api not installed!")

    def get_summary(self, topic, sentences=5):
        """
        Get Wikipedia summary

        Args:
            topic: What to look up
            sentences: How many sentences

        Returns:
            Summary text
        """
        if not WIKI_AVAILABLE or not self.wiki:
            return "❌ Wikipedia not installed! Run: pip install wikipedia-api"

        try:
            page = self.wiki.page(topic)

            if not page.exists():
                # Try search
                return f"📭 Wikipedia page for '{topic}' not found. Try different spelling!"

            summary = page.summary

            # Limit sentences
            parts = summary.split(". ")
            if len(parts) > sentences:
                summary = ". ".join(parts[:sentences]) + "."

            result = f"📚 Wikipedia — {page.title}:\n\n"
            result += f"   {summary}\n\n"
            result += f"   🔗 {page.fullurl}"

            log_event("Wikipedia", f"'{topic}' → {len(summary)} chars")
            return result

        except Exception as e:
            log_error(str(e), "WikiTool.get_summary")
            return f"❌ Wikipedia error: {e}"

    def search(self, query):
        """Search Wikipedia for pages"""
        if not WIKI_AVAILABLE or not self.wiki:
            return "❌ Wikipedia not installed!"

        try:
            page = self.wiki.page(query)

            if page.exists():
                return self.get_summary(query)

            return f"📭 No Wikipedia page found for '{query}'"

        except Exception as e:
            return f"❌ Error: {e}"

    def is_available(self):
        return WIKI_AVAILABLE and self.wiki is not None