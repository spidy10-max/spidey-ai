"""
Spidey AI — Tool Connector
Connects AI brain to computer tools
AI decides what tool to use based on user message!
"""
import re
from spidey.tools.computer import ComputerControl
from spidey.logger import app_logger, log_event, log_error


class ToolConnector:
    """
    Connects user commands to computer actions.
    Detects intent from natural language!

    Examples:
    "open Chrome" → opens Chrome
    "take a screenshot" → takes screenshot
    "search for readme files" → searches files
    "open youtube" → opens youtube.com
    "close notepad" → closes notepad
    """

    def __init__(self):
        self.pc = ComputerControl()
        self.enabled = True
        app_logger.info("ToolConnector initialized")

    def process_command(self, text):
        """
        Check if text contains a computer command
        If yes → execute it and return result
        If no → return None (let AI handle it)

        Args:
            text: User's message

        Returns:
            str result if command found, None otherwise
        """
        if not self.enabled:
            return None

        if not text or len(text.strip()) < 3:
            return None

        lower = text.lower().strip()

        # Try each detector
        result = None

        result = result or self._detect_open_app(lower)
        result = result or self._detect_close_app(lower)
        result = result or self._detect_screenshot(lower)
        result = result or self._detect_open_url(lower, text)
        result = result or self._detect_open_folder(lower, text)
        result = result or self._detect_search_files(lower, text)
        result = result or self._detect_type_text(lower, text)
        result = result or self._detect_keyboard(lower)
        result = result or self._detect_system(lower)

        return result

    # ============================================================
    #  OPEN APP
    # ============================================================

    def _detect_open_app(self, text):
        """Detect: open chrome, launch notepad, start calculator"""
        patterns = [
            r"(?:open|launch|start|run|chalo)\s+(.+?)(?:\s+please|\s+now|\s+karo)?$",
            r"(.+?)\s+(?:open|kholo|chala|karo)\s*$",
        ]

        # Known app names
        app_names = [
            "chrome", "google chrome", "browser",
            "notepad", "calculator", "calc", "paint",
            "cmd", "command prompt", "terminal", "powershell",
            "explorer", "file explorer", "files",
            "settings", "task manager",
            "vscode", "vs code", "visual studio code",
            "word", "excel", "powerpoint",
            "spotify", "discord",
            "snipping tool", "screenshot"
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                app = match.group(1).strip().lower()
                # Remove common words
                app = app.replace("please", "").replace("the", "").strip()

                # Check if it's a known app
                if app in app_names:
                    result = self.pc.open_app(app)
                    log_event("Tool: Open App", app)
                    return result

                # Check partial match
                for known in app_names:
                    if known in app or app in known:
                        result = self.pc.open_app(known)
                        log_event("Tool: Open App", known)
                        return result

        return None

    # ============================================================
    #  CLOSE APP
    # ============================================================

    def _detect_close_app(self, text):
        """Detect: close chrome, kill notepad, band karo"""
        patterns = [
            r"(?:close|kill|stop|quit|exit|band)\s+(.+?)(?:\s+please|\s+now|\s+karo)?$",
            r"(.+?)\s+(?:close|band|khatam)\s*(?:karo|kro)?$",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                app = match.group(1).strip().lower()
                app = app.replace("please", "").replace("the", "").strip()

                if len(app) > 1:
                    result = self.pc.close_app(app)
                    log_event("Tool: Close App", app)
                    return result

        return None

    # ============================================================
    #  SCREENSHOT
    # ============================================================

    def _detect_screenshot(self, text):
        """Detect: take screenshot, capture screen, ss lo"""
        keywords = [
            "take screenshot", "take a screenshot", "screenshot le",
            "screenshot lo", "capture screen", "screen capture",
            "ss lo", "ss le", "take ss", "screenshot"
        ]

        for kw in keywords:
            if kw in text:
                result = self.pc.take_screenshot()
                log_event("Tool: Screenshot", "taken")
                return result

        return None

    # ============================================================
    #  OPEN URL
    # ============================================================

    def _detect_open_url(self, lower, original):
        """Detect: open youtube, go to google, website kholo"""
        # Direct URLs
        url_match = re.search(r'(?:open|go to|visit)\s+(https?://\S+)', lower)
        if url_match:
            url = url_match.group(1)
            result = self.pc.open_url(url)
            log_event("Tool: Open URL", url)
            return result

        # Known websites
        websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "github": "https://github.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://twitter.com",
            "x": "https://x.com",
            "instagram": "https://www.instagram.com",
            "whatsapp": "https://web.whatsapp.com",
            "linkedin": "https://www.linkedin.com",
            "stackoverflow": "https://stackoverflow.com",
            "stack overflow": "https://stackoverflow.com",
            "chatgpt": "https://chat.openai.com",
            "claude": "https://claude.ai",
            "reddit": "https://www.reddit.com",
            "amazon": "https://www.amazon.com",
            "netflix": "https://www.netflix.com",
            "wikipedia": "https://www.wikipedia.org",
        }

        patterns = [
            r"(?:open|go to|visit|kholo)\s+(.+?)(?:\s+please|\s+now|\s+karo)?$",
            r"(.+?)\s+(?:kholo|open karo)\s*$",
        ]

        for pattern in patterns:
            match = re.search(pattern, lower)
            if match:
                site = match.group(1).strip()
                site = site.replace("please", "").replace("the", "").strip()

                if site in websites:
                    result = self.pc.open_url(websites[site])
                    log_event("Tool: Open Website", site)
                    return result

                # Check partial
                for name, url in websites.items():
                    if name in site or site in name:
                        result = self.pc.open_url(url)
                        log_event("Tool: Open Website", name)
                        return result

        return None

    # ============================================================
    #  OPEN FOLDER
    # ============================================================

    def _detect_open_folder(self, lower, original):
        """Detect: open downloads, open desktop, folder kholo"""
        folders = {
            "downloads": os.path.expanduser("~\\Downloads"),
            "desktop": os.path.expanduser("~\\Desktop"),
            "documents": os.path.expanduser("~\\Documents"),
            "pictures": os.path.expanduser("~\\Pictures"),
            "music": os.path.expanduser("~\\Music"),
            "videos": os.path.expanduser("~\\Videos"),
            "home": os.path.expanduser("~"),
            "c drive": "C:\\",
            "d drive": "D:\\",
        }

        patterns = [
            r"(?:open|show|go to)\s+(.+?)\s+(?:folder|directory)?",
            r"(.+?)\s+folder\s+(?:kholo|open)",
        ]

        for pattern in patterns:
            match = re.search(pattern, lower)
            if match:
                folder = match.group(1).strip()
                folder = folder.replace("please", "").replace("the", "").replace("my", "").strip()

                if folder in folders:
                    result = self.pc.open_folder(folders[folder])
                    log_event("Tool: Open Folder", folder)
                    return result

                # Check if it's a direct path
                if os.path.exists(folder):
                    result = self.pc.open_folder(folder)
                    return result

        return None

    # ============================================================
    #  SEARCH FILES
    # ============================================================

    def _detect_search_files(self, lower, original):
        """Detect: search for readme files, find python files"""
        patterns = [
            r"(?:search|find|look for|dhundo)\s+(?:for\s+)?(.+?)(?:\s+files?)?(?:\s+in\s+(.+))?$",
            r"(.+?)\s+(?:files?\s+)?(?:dhundo|khojo|search karo)",
        ]

        for pattern in patterns:
            match = re.search(pattern, lower)
            if match:
                query = match.group(1).strip()
                query = query.replace("please", "").replace("all", "").strip()

                if len(query) < 2:
                    continue

                # Determine search directory
                search_dir = os.path.expanduser("~")
                if match.lastindex and match.lastindex >= 2:
                    custom_dir = match.group(2)
                    if custom_dir and os.path.exists(custom_dir.strip()):
                        search_dir = custom_dir.strip()

                # Detect extension
                extension = None
                ext_map = {
                    "python": ".py", "py": ".py",
                    "text": ".txt", "txt": ".txt",
                    "pdf": ".pdf",
                    "word": ".docx", "doc": ".docx",
                    "image": ".png", "photo": ".jpg",
                    "video": ".mp4",
                    "music": ".mp3", "audio": ".mp3",
                    "json": ".json",
                    "csv": ".csv",
                    "html": ".html",
                    "markdown": ".md", "md": ".md",
                }

                for key, ext in ext_map.items():
                    if key in query:
                        extension = ext
                        query = query.replace(key, "").strip()
                        break

                if not query:
                    query = "*"

                files = self.pc.search_files(search_dir, query, extension=extension)

                if files:
                    result = f"📂 Found {len(files)} files:\n"
                    for f in files[:10]:
                        result += f"   📄 {f}\n"
                    if len(files) > 10:
                        result += f"   ... and {len(files)-10} more"
                    log_event("Tool: Search Files", f"{query} → {len(files)} found")
                    return result
                else:
                    return f"📭 No files found for '{query}'"

        return None

    # ============================================================
    #  TYPE TEXT
    # ============================================================

    def _detect_type_text(self, lower, original):
        """Detect: type hello world, likho ye text"""
        patterns = [
            r"(?:type|write|likho)\s+[\"'](.+?)[\"']",
            r"(?:type|write|likho)\s+(.+?)$",
        ]

        for pattern in patterns:
            match = re.search(pattern, lower)
            if match:
                text = match.group(1).strip()
                if len(text) > 1 and text not in ["something", "text", "kuch"]:
                    # Use original case
                    orig_match = re.search(pattern, original.lower())
                    if orig_match:
                        start = orig_match.start(1)
                        end = orig_match.end(1)
                        actual_text = original[start:end].strip()
                    else:
                        actual_text = text

                    result = self.pc.type_text(actual_text)
                    log_event("Tool: Type", actual_text[:30])
                    return result

        return None

    # ============================================================
    #  KEYBOARD
    # ============================================================

    def _detect_keyboard(self, text):
        """Detect: press enter, ctrl+c, alt+tab"""
        # Hotkeys
        hotkey_patterns = [
            (r"(?:press\s+)?ctrl\s*\+\s*c", ["ctrl", "c"]),
            (r"(?:press\s+)?ctrl\s*\+\s*v", ["ctrl", "v"]),
            (r"(?:press\s+)?ctrl\s*\+\s*z", ["ctrl", "z"]),
            (r"(?:press\s+)?ctrl\s*\+\s*s", ["ctrl", "s"]),
            (r"(?:press\s+)?ctrl\s*\+\s*a", ["ctrl", "a"]),
            (r"(?:press\s+)?alt\s*\+\s*tab", ["alt", "tab"]),
            (r"(?:press\s+)?alt\s*\+\s*f4", ["alt", "F4"]),
            (r"(?:press\s+)?ctrl\s*\+\s*shift\s*\+\s*esc", ["ctrl", "shift", "escape"]),
        ]

        for pattern, keys in hotkey_patterns:
            if re.search(pattern, text):
                result = self.pc.hotkey(*keys)
                log_event("Tool: Hotkey", "+".join(keys))
                return result

        # Single keys
        key_patterns = [
            (r"press\s+enter", "enter"),
            (r"press\s+escape", "escape"),
            (r"press\s+esc", "escape"),
            (r"press\s+tab", "tab"),
            (r"press\s+space", "space"),
            (r"press\s+backspace", "backspace"),
            (r"press\s+delete", "delete"),
        ]

        for pattern, key in key_patterns:
            if re.search(pattern, text):
                result = self.pc.press_key(key)
                log_event("Tool: Key", key)
                return result

        return None

    # ============================================================
    #  SYSTEM
    # ============================================================

    def _detect_system(self, text):
        """Detect: lock screen, volume up"""
        if "lock screen" in text or "lock computer" in text or "screen lock" in text:
            return self.pc.lock_screen()

        if "mouse position" in text or "mouse kahan" in text:
            return self.pc.get_mouse_position()

        if "screen size" in text or "resolution" in text:
            return self.pc.get_screen_size()

        return None

    # ============================================================
    #  TOGGLE
    # ============================================================

    def toggle(self):
        """Enable/disable tool connector"""
        self.enabled = not self.enabled
        return self.enabled

    def is_enabled(self):
        return self.enabled


# Need os for folder detection
import os