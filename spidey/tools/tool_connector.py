"""
Spidey AI — Tool Connector (Complete with Internet Tools!)
"""
import re
import os
from spidey.tools.computer import ComputerControl
from spidey.tools.file_manager import FileManager
from spidey.tools.system_info import SystemInfo
from spidey.tools.internet.weather import WeatherTool
from spidey.tools.internet.search import SearchTool
from spidey.tools.internet.wiki import WikiTool
from spidey.logger import app_logger, log_event, log_error


class ToolConnector:
    """AI to all tools bridge"""

    def __init__(self):
        self.pc = ComputerControl()
        self.fm = FileManager()
        self.si = SystemInfo()
        self.weather = WeatherTool()
        self.search = SearchTool()
        self.wiki = WikiTool()
        self.enabled = True
        app_logger.info("ToolConnector initialized (full + internet)")

    def process_command(self, text):
        """Check text for commands"""
        if not self.enabled or not text or len(text.strip()) < 3:
            return None

        lower = text.lower().strip()

        result = None
        result = result or self._detect_weather(lower)
        result = result or self._detect_web_search(lower)
        result = result or self._detect_news(lower)
        result = result or self._detect_wikipedia(lower)
        result = result or self._detect_open_app(lower)
        result = result or self._detect_close_app(lower)
        result = result or self._detect_screenshot(lower)
        result = result or self._detect_recording(lower)
        result = result or self._detect_open_url(lower, text)
        result = result or self._detect_browser(lower)
        result = result or self._detect_open_folder(lower)
        result = result or self._detect_file_search(lower)
        result = result or self._detect_file_operations(lower, text)
        result = result or self._detect_disk_info(lower)
        result = result or self._detect_type_text(lower, text)
        result = result or self._detect_keyboard(lower)
        result = result or self._detect_window(lower)
        result = result or self._detect_scroll(lower)
        result = result or self._detect_system(lower)
        result = result or self._detect_system_info(lower)

        return result

    # ============================================================
    #  INTERNET TOOLS
    # ============================================================

    def _detect_weather(self, text):
        """weather in kotaddu, mausam, weather report"""
        patterns = [
            r"weather\s+(?:in\s+)?(.+?)$",
            r"mausam\s+(.+?)$",
            r"temperature\s+(?:in\s+)?(.+?)$",
            r"(.+?)\s+(?:ka\s+)?(?:weather|mausam)$",
            r"how(?:'s|\s+is)\s+(?:the\s+)?weather\s+(?:in\s+)?(.+?)$",
            r"what(?:'s|\s+is)\s+(?:the\s+)?weather\s+(?:in\s+)?(.+?)$",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                city = match.group(1).strip()
                city = city.replace("please", "").replace("today", "").replace("now", "").strip()
                if len(city) > 1:
                    return self.weather.get_weather(city)

        # Just "weather" → use default city
        if text.strip() in ["weather", "mausam", "weather today", "aaj ka mausam"]:
            return self.weather.get_weather("Kotaddu")

        # Forecast
        forecast_match = re.search(r"(?:forecast|prediction)\s+(?:for\s+)?(.+?)$", text)
        if forecast_match:
            city = forecast_match.group(1).strip()
            return self.weather.get_forecast(city)

        return None

    def _detect_web_search(self, text):
        """search for python, google something"""
        patterns = [
            r"(?:web\s+)?search\s+(?:for\s+)?(.+?)$",
            r"google\s+(.+?)$",
            r"search\s+(?:the\s+)?(?:web|internet)\s+(?:for\s+)?(.+?)$",
            r"look\s+up\s+(.+?)$",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                query = match.group(1).strip()
                if len(query) > 1:
                    # Check if it's a google search (open browser) vs web search (get results)
                    if "google" in text and "search" not in text:
                        continue  # Let browser handler take it
                    return self.search.search(query)

        return None

    def _detect_news(self, text):
        """news about pakistan, latest news, headlines"""
        patterns = [
            r"news\s+(?:about\s+)?(.+?)$",
            r"(?:latest|today'?s?)\s+news\s*(?:about\s+)?(.+?)?$",
            r"headlines\s*(?:about\s+)?(.+?)?$",
            r"khabar(?:en)?\s+(.+?)?$",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                query = match.group(1).strip() if match.group(1) else "world"
                query = query.replace("please", "").strip()
                if not query:
                    query = "world"
                return self.search.search_news(query)

        if text.strip() in ["news", "headlines", "latest news", "khabaren", "today news"]:
            return self.search.search_news("world")

        return None

    def _detect_wikipedia(self, text):
        """wikipedia python, wiki about AI, define machine learning"""
        patterns = [
            r"(?:wikipedia|wiki)\s+(?:about\s+)?(.+?)$",
            r"(?:define|definition\s+of)\s+(.+?)$",
            r"what\s+is\s+(.+?)(?:\s+in\s+detail)?$",
            r"tell\s+me\s+about\s+(.+?)$",
            r"explain\s+(.+?)$",
            r"(.+?)\s+(?:kya\s+hai|kya\s+he)$",
        ]

        # Only use wikipedia for knowledge queries, not commands
        skip_words = ["weather", "time", "battery", "wifi", "screenshot",
                       "open", "close", "search", "find", "news", "your", "my"]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                topic = match.group(1).strip()
                topic = topic.replace("please", "").replace("?", "").strip()

                if len(topic) > 1 and not any(sw in topic.lower() for sw in skip_words):
                    return self.wiki.get_summary(topic)

        return None

    # ============================================================
    #  COMPUTER TOOLS (same as before)
    # ============================================================

    def _detect_open_app(self, text):
        apps = [
            "chrome", "google chrome", "browser",
            "firefox", "edge", "brave",
            "notepad", "calculator", "calc", "paint",
            "cmd", "command prompt", "terminal", "powershell",
            "explorer", "file explorer", "files",
            "settings", "task manager",
            "vscode", "vs code", "visual studio code",
            "word", "excel", "powerpoint", "outlook",
            "spotify", "discord", "telegram", "whatsapp",
            "zoom", "teams", "vlc", "obs",
            "snipping tool", "camera", "photos", "store",
            "control panel",
        ]

        patterns = [
            r"(?:open|launch|start|run|chalo|kholo)\s+(.+?)(?:\s+please|\s+now|\s+karo|\s+kro)?$",
            r"(.+?)\s+(?:open|kholo|chala|karo|kro)\s*$",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                app = match.group(1).strip().replace("please", "").replace("the", "").strip()
                if app in apps:
                    if app in ["chrome", "google chrome", "browser"]:
                        return self.pc.open_chrome()
                    return self.pc.open_app(app)
                for known in apps:
                    if known in app or app in known:
                        if known in ["chrome", "google chrome", "browser"]:
                            return self.pc.open_chrome()
                        return self.pc.open_app(known)
        return None

    def _detect_close_app(self, text):
        patterns = [
            r"(?:close|kill|stop|band|quit)\s+(.+?)(?:\s+please|\s+now|\s+karo|\s+kro)?$",
            r"(.+?)\s+(?:close|band|khatam)\s*(?:karo|kro)?$",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                app = match.group(1).strip().replace("please", "").strip()
                if len(app) > 1 and app not in ["the", "a", "this", "that"]:
                    return self.pc.close_app(app)
        return None

    def _detect_screenshot(self, text):
        keywords = ["take screenshot", "take a screenshot", "screenshot le",
                     "screenshot lo", "capture screen", "ss lo", "ss le",
                     "take ss", "screenshot karo"]
        if text.strip() == "screenshot" or any(kw in text for kw in keywords):
            return self.pc.take_screenshot()
        return None

    def _detect_recording(self, text):
        if any(kw in text for kw in ["start recording", "record screen",
                                      "screen record", "record karo", "recording shuru"]):
            dur = re.search(r"(\d+)\s*(?:sec|second|minute|min)", text)
            if dur:
                d = int(dur.group(1))
                if "min" in text:
                    d *= 60
                return self.pc.start_recording(duration=d)
            return self.pc.start_recording()

        if any(kw in text for kw in ["stop recording", "recording stop", "recording band"]):
            return self.pc.stop_recording()

        match = re.search(r"record\s+(?:for\s+)?(\d+)\s*(?:sec|second|minute|min)", text)
        if match:
            d = int(match.group(1))
            if "min" in text:
                d *= 60
            return self.pc.record_for(d)
        return None

    def _detect_open_url(self, lower, original):
        websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "github": "https://github.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://twitter.com",
            "instagram": "https://www.instagram.com",
            "whatsapp web": "https://web.whatsapp.com",
            "linkedin": "https://www.linkedin.com",
            "stackoverflow": "https://stackoverflow.com",
            "chatgpt": "https://chat.openai.com",
            "claude": "https://claude.ai",
            "reddit": "https://www.reddit.com",
            "amazon": "https://www.amazon.com",
            "netflix": "https://www.netflix.com",
            "wikipedia": "https://www.wikipedia.org",
            "daraz": "https://www.daraz.pk",
        }

        url_match = re.search(r'(?:open|go to|visit)\s+(https?://\S+)', lower)
        if url_match:
            return self.pc.open_chrome(url_match.group(1))

        patterns = [r"(?:open|go to|visit|kholo)\s+(.+?)(?:\s+please|\s+now|\s+karo)?$"]
        for pattern in patterns:
            match = re.search(pattern, lower)
            if match:
                site = match.group(1).strip().replace("please", "").strip()
                if site in websites:
                    return self.pc.open_chrome(websites[site])
                for name, url in websites.items():
                    if name in site or site in name:
                        return self.pc.open_chrome(url)
        return None

    def _detect_browser(self, text):
        match = re.search(r"(?:google|search for)\s+(.+?)$", text)
        if match:
            query = match.group(1).strip()
            if len(query) > 1:
                return self.pc.chrome_search(query)
        if "new tab" in text:
            return self.pc.chrome_new_tab()
        return None

    def _detect_open_folder(self, lower):
        folders = {
            "downloads": os.path.expanduser("~\\Downloads"),
            "desktop": os.path.expanduser("~\\Desktop"),
            "documents": os.path.expanduser("~\\Documents"),
            "pictures": os.path.expanduser("~\\Pictures"),
            "music": os.path.expanduser("~\\Music"),
            "videos": os.path.expanduser("~\\Videos"),
            "home": os.path.expanduser("~"),
            "c drive": "C:\\", "d drive": "D:\\", "k drive": "K:\\",
        }
        for name, path in folders.items():
            if f"open {name}" in lower or f"{name} kholo" in lower:
                if os.path.exists(path):
                    return self.pc.open_folder(path)
        return None

    def _detect_file_search(self, lower):
        ext_match = re.search(r"(?:find|show|list)\s+(?:all\s+)?(\w+)\s+files", lower)
        if ext_match:
            ext_name = ext_match.group(1).strip()
            ext_map = {"python": ".py", "text": ".txt", "pdf": ".pdf", "word": ".docx",
                       "image": ".png", "video": ".mp4", "music": ".mp3", "json": ".json",
                       "html": ".html", "excel": ".xlsx", "zip": ".zip"}
            if ext_name in ext_map:
                results = self.fm.search_by_extension(ext_map[ext_name])
                return self.fm.format_results(results, f"{ext_name.upper()} Files")

        if any(kw in lower for kw in ["recent files", "latest files", "naye files"]):
            return self.fm.format_results(self.fm.search_recent(hours=24), "Recent Files")

        if any(kw in lower for kw in ["large files", "big files", "heavy files"]):
            return self.fm.format_results(self.fm.search_large_files(min_size_mb=50), "Large Files")

        match = re.search(r"(?:find|dhundo|khojo)\s+(?:for\s+)?(.+?)(?:\s+files?)?$", lower)
        if match:
            query = match.group(1).strip()
            if len(query) > 1 and query not in ["the", "a", "my", "all"]:
                return self.fm.format_results(self.fm.search(query), f"'{query}'")

        list_match = re.search(r"(?:list|dikhao)\s+(.+?)(?:\s+files)?$", lower)
        if list_match:
            folder = list_match.group(1).strip()
            folder_map = {"downloads": "~\\Downloads", "desktop": "~\\Desktop", "documents": "~\\Documents"}
            if folder in folder_map:
                items = self.fm.list_folder(os.path.expanduser(folder_map[folder]))
                output = f"📂 {folder.title()} ({len(items)}):\n"
                for item in items[:15]:
                    output += f"   {item['icon']} {item['name']} ({item['size_str']})\n"
                return output
        return None

    def _detect_file_operations(self, lower, original):
        match = re.search(r"(?:create|make|bana)\s+(?:a\s+)?folder\s+(.+?)$", lower)
        if match:
            name = match.group(1).strip()
            return self.fm.create_folder(os.path.join(os.path.expanduser("~\\Desktop"), name))
        return None

    def _detect_disk_info(self, lower):
        if any(kw in lower for kw in ["disk space", "storage space", "free space", "disk info"]):
            drives = ["C:"] + [f"{d}:" for d in "DEFK" if os.path.exists(f"{d}:\\")]
            output = "💾 Disk:\n"
            for drive in drives:
                info = self.fm.get_disk_space(drive)
                if isinstance(info, dict):
                    output += f"   {drive} — {info['free']} free / {info['total']} ({info['percent_used']}%)\n"
            return output
        return None

    def _detect_type_text(self, lower, original):
        match = re.search(r"(?:type|write|likho)\s+[\"'](.+?)[\"']", lower)
        if match:
            return self.pc.type_text(match.group(1))
        match = re.search(r"(?:type|write|likho)\s+(.+?)$", lower)
        if match:
            t = match.group(1).strip()
            if len(t) > 1 and t not in ["something", "text", "kuch"]:
                return self.pc.type_text(t)
        return None

    def _detect_keyboard(self, text):
        hotkeys = [
            (r"ctrl\s*\+\s*c", ["ctrl", "c"]), (r"ctrl\s*\+\s*v", ["ctrl", "v"]),
            (r"ctrl\s*\+\s*z", ["ctrl", "z"]), (r"ctrl\s*\+\s*s", ["ctrl", "s"]),
            (r"alt\s*\+\s*tab", ["alt", "tab"]), (r"alt\s*\+\s*f4", ["alt", "F4"]),
        ]
        for p, k in hotkeys:
            if re.search(p, text):
                return self.pc.hotkey(*k)
        keys = [(r"press\s+enter", "enter"), (r"press\s+escape", "escape"),
                (r"press\s+tab", "tab"), (r"press\s+space", "space")]
        for p, k in keys:
            if re.search(p, text):
                return self.pc.press_key(k)
        return None

    def _detect_window(self, text):
        if "minimize" in text: return self.pc.minimize_window()
        if "maximize" in text or "full screen" in text: return self.pc.maximize_window()
        if "switch window" in text or "alt tab" in text: return self.pc.switch_window()
        if "show desktop" in text: return self.pc.show_desktop()
        if "close window" in text: return self.pc.close_window()
        if "snap left" in text: return self.pc.snap_left()
        if "snap right" in text: return self.pc.snap_right()
        return None

    def _detect_scroll(self, text):
        if "scroll up" in text: return self.pc.scroll(5)
        if "scroll down" in text: return self.pc.scroll(-5)
        return None

    def _detect_system(self, text):
        if "lock screen" in text: return self.pc.lock_screen()
        if "mouse position" in text: return self.pc.get_mouse_position()
        if "screen size" in text or "resolution" in text: return self.pc.get_screen_size()
        match = re.search(r"brightness\s*(\d+)", text)
        if match: return self.pc.set_brightness(int(match.group(1)))
        return None

    def _detect_system_info(self, text):
        if any(kw in text for kw in ["system info", "pc info", "computer info", "about my pc"]):
            return self.si.get_all_info()
        if any(kw in text for kw in ["battery", "charge", "battery status"]):
            return self.si.get_battery()
        if any(kw in text for kw in ["wifi", "network", "internet status", "wifi name"]):
            return self.si.get_wifi()
        if any(kw in text for kw in ["my ip", "ip address"]):
            return self.si.get_ip()
        if any(kw in text for kw in ["uptime", "how long running"]):
            return self.si.get_uptime()
        if any(kw in text for kw in ["running apps", "open apps", "active apps"]):
            return self.si.get_running_apps()
        if any(kw in text for kw in ["what time", "kya time", "date and time", "today date"]):
            return self.si.get_date_time()
        if any(kw in text for kw in ["quick info", "system status", "pc status"]):
            return self.si.get_quick_info()
        return None

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def is_enabled(self):
        return self.enabled