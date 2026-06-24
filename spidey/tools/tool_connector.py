"""
Spidey AI — Tool Connector (Enhanced!)
Detects commands from natural language
"""
import re
import os
from spidey.tools.computer import ComputerControl
from spidey.logger import app_logger, log_event, log_error


class ToolConnector:
    """Enhanced AI to computer bridge"""

    def __init__(self):
        self.pc = ComputerControl()
        self.enabled = True
        app_logger.info("ToolConnector initialized")

    def process_command(self, text):
        """Check text for computer commands"""
        if not self.enabled or not text or len(text.strip()) < 3:
            return None

        lower = text.lower().strip()

        result = None
        result = result or self._detect_open_app(lower)
        result = result or self._detect_close_app(lower)
        result = result or self._detect_screenshot(lower)
        result = result or self._detect_recording(lower)
        result = result or self._detect_open_url(lower, text)
        result = result or self._detect_browser(lower)
        result = result or self._detect_open_folder(lower)
        result = result or self._detect_search_files(lower)
        result = result or self._detect_type_text(lower, text)
        result = result or self._detect_keyboard(lower)
        result = result or self._detect_window(lower)
        result = result or self._detect_system(lower)
        result = result or self._detect_scroll(lower)

        return result

    def _detect_open_app(self, text):
        """open chrome, launch notepad, start calculator"""
        apps = [
            "chrome", "google chrome", "browser", "google",
            "firefox", "edge", "brave",
            "notepad", "calculator", "calc", "paint",
            "cmd", "command prompt", "terminal", "powershell",
            "explorer", "file explorer", "files",
            "settings", "task manager",
            "vscode", "vs code", "visual studio code",
            "word", "excel", "powerpoint", "outlook",
            "spotify", "discord", "telegram", "whatsapp",
            "zoom", "teams", "vlc", "obs", "obs studio",
            "snipping tool", "camera", "photos", "store",
            "control panel", "device manager",
        ]

        patterns = [
            r"(?:open|launch|start|run|chalo|kholo)\s+(.+?)(?:\s+please|\s+now|\s+karo|\s+kro)?$",
            r"(.+?)\s+(?:open|kholo|chala|karo|kro)\s*$",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                app = match.group(1).strip()
                app = app.replace("please", "").replace("the", "").strip()

                # Direct match
                if app in apps:
                    if app in ["chrome", "google chrome", "google", "browser"]:
                        return self.pc.open_chrome()
                    return self.pc.open_app(app)

                # Partial match
                for known in apps:
                    if known in app or app in known:
                        if known in ["chrome", "google chrome", "google", "browser"]:
                            return self.pc.open_chrome()
                        return self.pc.open_app(known)

        return None

    def _detect_close_app(self, text):
        """close chrome, kill notepad"""
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
        """take screenshot, ss lo"""
        keywords = [
            "take screenshot", "take a screenshot", "screenshot le",
            "screenshot lo", "capture screen", "screen capture",
            "ss lo", "ss le", "take ss", "screenshot lelo",
            "screenshot karo", "screencapture"
        ]
        if any(kw in text for kw in keywords):
            return self.pc.take_screenshot()

        # Just "screenshot" alone
        if text.strip() == "screenshot":
            return self.pc.take_screenshot()

        return None

    def _detect_recording(self, text):
        """start recording, stop recording, record for 30 seconds"""
        if any(kw in text for kw in ["start recording", "record screen", "recording start",
                                      "screen record", "record karo", "recording shuru"]):
            # Check for duration
            dur_match = re.search(r"(\d+)\s*(?:sec|second|minute|min)", text)
            if dur_match:
                duration = int(dur_match.group(1))
                if "min" in text:
                    duration *= 60
                return self.pc.start_recording(duration=duration)
            return self.pc.start_recording()

        if any(kw in text for kw in ["stop recording", "recording stop", "recording band",
                                      "record stop", "recording ruko"]):
            return self.pc.stop_recording()

        # "record for 30 seconds"
        match = re.search(r"record\s+(?:for\s+)?(\d+)\s*(?:sec|second|minute|min)", text)
        if match:
            duration = int(match.group(1))
            if "min" in text:
                duration *= 60
            return self.pc.record_for(duration)

        return None

    def _detect_open_url(self, lower, original):
        """open youtube, go to google"""
        websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "github": "https://github.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://twitter.com",
            "x": "https://x.com",
            "instagram": "https://www.instagram.com",
            "whatsapp web": "https://web.whatsapp.com",
            "linkedin": "https://www.linkedin.com",
            "stackoverflow": "https://stackoverflow.com",
            "stack overflow": "https://stackoverflow.com",
            "chatgpt": "https://chat.openai.com",
            "claude": "https://claude.ai",
            "reddit": "https://www.reddit.com",
            "amazon": "https://www.amazon.com",
            "netflix": "https://www.netflix.com",
            "wikipedia": "https://www.wikipedia.org",
            "daraz": "https://www.daraz.pk",
        }

        # Direct URL
        url_match = re.search(r'(?:open|go to|visit)\s+(https?://\S+)', lower)
        if url_match:
            return self.pc.open_chrome(url_match.group(1))

        patterns = [
            r"(?:open|go to|visit|kholo)\s+(.+?)(?:\s+please|\s+now|\s+karo)?$",
        ]

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
        """search on google, new tab"""
        # Google search
        match = re.search(r"(?:google|search|search for|google search)\s+(.+?)$", text)
        if match:
            query = match.group(1).strip()
            if len(query) > 1:
                return self.pc.chrome_search(query)

        if "new tab" in text:
            return self.pc.chrome_new_tab()

        return None

    def _detect_open_folder(self, lower):
        """open downloads, open desktop"""
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
            "k drive": "K:\\",
        }

        for name, path in folders.items():
            if f"open {name}" in lower or f"{name} kholo" in lower:
                if os.path.exists(path):
                    return self.pc.open_folder(path)
        return None

    def _detect_search_files(self, lower):
        """search for readme files"""
        match = re.search(r"(?:search|find|dhundo|khojo)\s+(?:for\s+)?(.+?)(?:\s+files?)?$", lower)
        if match:
            query = match.group(1).strip()
            if len(query) > 1 and query not in ["the", "a", "my"]:
                files = self.pc.search_files(os.path.expanduser("~"), query)
                if files:
                    result = f"📂 Found {len(files)} files:\n"
                    for f in files[:10]:
                        result += f"   📄 {f}\n"
                    return result
                return f"📭 No files found for '{query}'"
        return None

    def _detect_type_text(self, lower, original):
        """type hello world"""
        match = re.search(r"(?:type|write|likho)\s+[\"'](.+?)[\"']", lower)
        if match:
            return self.pc.type_text(match.group(1))

        match = re.search(r"(?:type|write|likho)\s+(.+?)$", lower)
        if match:
            text = match.group(1).strip()
            if len(text) > 1 and text not in ["something", "text", "kuch"]:
                return self.pc.type_text(text)
        return None

    def _detect_keyboard(self, text):
        """press enter, ctrl+c"""
        hotkeys = [
            (r"(?:press\s+)?ctrl\s*\+\s*c", ["ctrl", "c"]),
            (r"(?:press\s+)?ctrl\s*\+\s*v", ["ctrl", "v"]),
            (r"(?:press\s+)?ctrl\s*\+\s*z", ["ctrl", "z"]),
            (r"(?:press\s+)?ctrl\s*\+\s*s", ["ctrl", "s"]),
            (r"(?:press\s+)?ctrl\s*\+\s*a", ["ctrl", "a"]),
            (r"(?:press\s+)?alt\s*\+\s*tab", ["alt", "tab"]),
            (r"(?:press\s+)?alt\s*\+\s*f4", ["alt", "F4"]),
        ]
        for pattern, keys in hotkeys:
            if re.search(pattern, text):
                return self.pc.hotkey(*keys)

        keys = [
            (r"press\s+enter", "enter"),
            (r"press\s+escape", "escape"),
            (r"press\s+esc", "escape"),
            (r"press\s+tab", "tab"),
            (r"press\s+space", "space"),
            (r"press\s+backspace", "backspace"),
            (r"press\s+delete", "delete"),
        ]
        for pattern, key in keys:
            if re.search(pattern, text):
                return self.pc.press_key(key)
        return None

    def _detect_window(self, text):
        """minimize, maximize, switch window"""
        if any(kw in text for kw in ["minimize", "minimize window", "chhota karo"]):
            return self.pc.minimize_window()
        if any(kw in text for kw in ["maximize", "maximize window", "bara karo", "full screen"]):
            return self.pc.maximize_window()
        if any(kw in text for kw in ["switch window", "alt tab", "next window"]):
            return self.pc.switch_window()
        if any(kw in text for kw in ["show desktop", "desktop dikhao"]):
            return self.pc.show_desktop()
        if any(kw in text for kw in ["close window", "window close", "band karo window"]):
            return self.pc.close_window()
        if "snap left" in text:
            return self.pc.snap_left()
        if "snap right" in text:
            return self.pc.snap_right()
        return None

    def _detect_scroll(self, text):
        """scroll up, scroll down"""
        if any(kw in text for kw in ["scroll up", "upar scroll"]):
            return self.pc.scroll(5)
        if any(kw in text for kw in ["scroll down", "neeche scroll"]):
            return self.pc.scroll(-5)
        return None

    def _detect_system(self, text):
        """lock screen, brightness"""
        if any(kw in text for kw in ["lock screen", "lock computer", "screen lock"]):
            return self.pc.lock_screen()
        if "mouse position" in text:
            return self.pc.get_mouse_position()
        if any(kw in text for kw in ["screen size", "resolution"]):
            return self.pc.get_screen_size()
        if any(kw in text for kw in ["sleep", "computer sleep", "hibernate"]):
            return self.pc.sleep_computer()
        if "empty recycle" in text or "recycle bin" in text:
            return self.pc.empty_recycle_bin()

        # Brightness
        match = re.search(r"(?:brightness|bright)\s*(\d+)", text)
        if match:
            return self.pc.set_brightness(int(match.group(1)))

        return None

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def is_enabled(self):
        return self.enabled