"""
Spidey AI — YouTube Search Tool
Search YouTube videos — FREE, no API key!
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


class YouTubeTool:
    """Search YouTube videos using DuckDuckGo"""

    def __init__(self):
        if DDGS_AVAILABLE:
            app_logger.info("YouTubeTool ready")
        else:
            app_logger.warning("YouTubeTool: ddgs not installed!")

    def search(self, query, max_results=5):
        """
        Search YouTube videos

        Args:
            query: What to search
            max_results: How many results

        Returns:
            Formatted results
        """
        if not DDGS_AVAILABLE:
            return "❌ Search not installed! Run: pip install ddgs"

        try:
            # Search YouTube via DuckDuckGo
            yt_query = f"site:youtube.com {query}"

            results = list(DDGS().text(yt_query, max_results=max_results))

            if not results:
                return f"📭 No YouTube videos found for '{query}'"

            output = f"🎬 YouTube Results for '{query}':\n\n"

            for i, r in enumerate(results, 1):
                title = r.get("title", "No title")
                body = r.get("body", "")
                url = r.get("href", "")

                output += f"   {i}. 🎥 {title}\n"
                if body:
                    output += f"      {body[:80]}...\n"
                if url:
                    output += f"      🔗 {url}\n"
                output += "\n"

            log_event("YouTube search", f"'{query}' → {len(results)}")
            return output.strip()

        except Exception as e:
            log_error(str(e), "YouTubeTool.search")
            return f"❌ YouTube search error: {e}"

    def get_video_url(self, query):
        """
        Get first YouTube video URL for a query

        Args:
            query: What to search

        Returns:
            URL string or error
        """
        if not DDGS_AVAILABLE:
            return None

        try:
            yt_query = f"site:youtube.com {query}"
            results = list(DDGS().text(yt_query, max_results=1))

            if results:
                url = results[0].get("href", "")
                if "youtube.com" in url or "youtu.be" in url:
                    return url

            return None

        except Exception as e:
            log_error(str(e), "YouTubeTool.get_video_url")
            return None

    def play_video(self, query):
        """
        Search and open first YouTube video in browser

        Args:
            query: What to search
        """
        try:
            url = self.get_video_url(query)

            if url:
                import webbrowser
                webbrowser.open(url)
                log_event("YouTube play", f"'{query}' → {url}")
                return f"🎬 Playing: {url}"
            else:
                # Fallback: open YouTube search page
                import webbrowser
                search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                return f"🎬 Opening YouTube search for '{query}'"

        except Exception as e:
            log_error(str(e), "YouTubeTool.play_video")
            return f"❌ Error: {e}"

    def is_available(self):
        return DDGS_AVAILABLE