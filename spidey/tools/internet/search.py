"""
Spidey AI — Web Search Tool
Search using ddgs (new DuckDuckGo package)
"""
from spidey.logger import app_logger, log_event, log_error

try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    try:
        from duckduckgo_search import DDGS
        DDGS_AVAILABLE = True
    except ImportError:
        DDGS_AVAILABLE = False


class SearchTool:
    """Web search — FREE!"""

    def __init__(self):
        if DDGS_AVAILABLE:
            app_logger.info("SearchTool ready")
        else:
            app_logger.warning("SearchTool: ddgs not installed! Run: pip install ddgs")

    def search(self, query, max_results=5):
        """Search the web"""
        if not DDGS_AVAILABLE:
            return "❌ Search not installed! Run: pip install ddgs"

        try:
            results = list(DDGS().text(query, max_results=max_results))

            if not results:
                return f"📭 No results for '{query}'"

            output = f"🔍 Results for '{query}':\n\n"
            for i, r in enumerate(results, 1):
                title = r.get("title", "")
                body = r.get("body", "")
                url = r.get("href", "")
                output += f"   {i}. {title}\n"
                output += f"      {body[:100]}...\n"
                if url:
                    output += f"      🔗 {url}\n"
                output += "\n"

            log_event("Search", f"'{query}' → {len(results)}")
            return output.strip()

        except Exception as e:
            log_error(str(e), "SearchTool.search")
            return f"❌ Search error: {e}"

    def search_news(self, query, max_results=5):
        """Search news"""
        if not DDGS_AVAILABLE:
            return "❌ Not installed!"

        try:
            results = list(DDGS().news(query, max_results=max_results))

            if not results:
                return f"📭 No news for '{query}'"

            output = f"📰 News for '{query}':\n\n"
            for i, r in enumerate(results, 1):
                title = r.get("title", "")
                body = r.get("body", "")
                source = r.get("source", "")
                date = r.get("date", "")
                output += f"   {i}. {title}\n"
                if body:
                    output += f"      {body[:80]}...\n"
                output += f"      📰 {source}"
                if date:
                    output += f" — {date[:10]}"
                output += "\n\n"

            log_event("News", f"'{query}' → {len(results)}")
            return output.strip()

        except Exception as e:
            log_error(str(e), "SearchTool.search_news")
            return f"❌ News error: {e}"

    def is_available(self):
        return DDGS_AVAILABLE