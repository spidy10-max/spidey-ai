"""
Spidey AI — Tool Connector (Enhanced with File Manager!)
"""
import re
import os
from spidey.tools.computer import ComputerControl
from spidey.tools.file_manager import FileManager
from spidey.logger import app_logger, log_event, log_error


class ToolConnector:
    """AI to computer + files bridge"""

    def __init__(self):
        self.pc = ComputerControl()
        self.fm = FileManager()
        self.enabled = True
        app_logger.info("ToolConnector initialized (with FileManager)")

    def process_command(self, text):
        """Check text for commands"""
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
        result = result or self._detect_file_search(lower)
        result = result or self._detect_file_operations(lower, text)
        result = result or self._detect_disk_info(lower)
        result = result or self._detect_type_text(lower, text)
        result = result or self._detect_keyboard(lower)
        result = result or self._detect_window(lower)
        result = result or self._detect_scroll(lower)
        result = result or self._detect_system(lower)

        return result

    def _detect_open_app(self, text):
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
                    if app in ["chrome", "google chrome", "google", "browser"]:
                        return self.pc.open_chrome()
                    return self.pc.open_app(app)
                for known in apps:
                    if known in app or app in known:
                        if known in ["chrome", "google chrome", "google", "browser"]:
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
        keywords = [
            "take screenshot", "take a screenshot", "screenshot le",
            "screenshot lo", "capture screen", "ss lo", "ss le",
            "take ss", "screenshot karo", "screenshot"
        ]
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

        if any(kw in text for kw in ["stop recording", "recording stop",
                                      "recording band", "record stop"]):
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
        match = re.search(r"(?:google|search|search for|google search)\s+(.+?)$", text)
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
            "c drive": "C:\\",
            "d drive": "D:\\",
            "k drive": "K:\\",
        }
        for name, path in folders.items():
            if f"open {name}" in lower or f"{name} kholo" in lower:
                if os.path.exists(path):
                    return self.pc.open_folder(path)
        return None

    def _detect_file_search(self, lower):
        """Enhanced file search — type, recent, large files"""

        # Search by extension: "find all python files", "show pdf files"
        ext_match = re.search(r"(?:find|show|list|search)\s+(?:all\s+)?(\w+)\s+files", lower)
        if ext_match:
            ext_name = ext_match.group(1).strip()
            ext_map = {
                "python": ".py", "py": ".py",
                "text": ".txt", "txt": ".txt",
                "pdf": ".pdf",
                "word": ".docx", "doc": ".docx",
                "image": ".png", "photo": ".jpg", "picture": ".jpg",
                "video": ".mp4", "mp4": ".mp4",
                "music": ".mp3", "audio": ".mp3", "mp3": ".mp3",
                "json": ".json", "csv": ".csv",
                "html": ".html", "markdown": ".md", "md": ".md",
                "excel": ".xlsx", "zip": ".zip",
                "exe": ".exe", "java": ".java",
                "javascript": ".js", "js": ".js",
                "css": ".css",
            }
            if ext_name in ext_map:
                results = self.fm.search_by_extension(ext_map[ext_name])
                return self.fm.format_results(results, f"{ext_name.upper()} Files")

        # Recent files: "show recent files", "recently modified"
        if any(kw in lower for kw in ["recent files", "recently modified", "latest files",
                                       "naye files", "new files"]):
            results = self.fm.search_recent(hours=24)
            return self.fm.format_results(results, "Recent Files (24 hours)")

        # Large files: "find large files", "big files"
        if any(kw in lower for kw in ["large files", "big files", "bade files",
                                       "heavy files"]):
            results = self.fm.search_large_files(min_size_mb=50)
            return self.fm.format_results(results, "Large Files (>50MB)")

        # General search: "search for readme", "find project files"
        match = re.search(r"(?:search|find|dhundo|khojo)\s+(?:for\s+)?(.+?)(?:\s+files?)?$", lower)
        if match:
            query = match.group(1).strip()
            if len(query) > 1 and query not in ["the", "a", "my", "all"]:
                results = self.fm.search(query)
                return self.fm.format_results(results, f"Files matching '{query}'")

        # List folder: "list downloads", "show desktop files"
        list_match = re.search(r"(?:list|show|dikhao)\s+(.+?)(?:\s+files|\s+folder)?$", lower)
        if list_match:
            folder = list_match.group(1).strip()
            folder_map = {
                "downloads": os.path.expanduser("~\\Downloads"),
                "desktop": os.path.expanduser("~\\Desktop"),
                "documents": os.path.expanduser("~\\Documents"),
            }
            if folder in folder_map:
                items = self.fm.list_folder(folder_map[folder])
                output = f"📂 {folder.title()} ({len(items)} items):\n"
                for item in items[:15]:
                    output += f"   {item['icon']} {item['name']} ({item['size_str']})\n"
                return output

        return None

    def _detect_file_operations(self, lower, original):
        """file info, folder size, create folder"""
        # Disk space
        if any(kw in lower for kw in ["disk space", "storage", "drive space",
                                       "free space", "disk info"]):
            drives = ["C:"]
            for d in ["D:", "E:", "K:"]:
                if os.path.exists(d + "\\"):
                    drives.append(d)

            output = "💾 Disk Space:\n"
            for drive in drives:
                info = self.fm.get_disk_space(drive)
                if isinstance(info, dict):
                    output += f"   {drive} — {info['free']} free / {info['total']} total ({info['percent_used']}% used)\n"
            return output

        # Create folder
        match = re.search(r"(?:create|make|bana)\s+(?:a\s+)?folder\s+(.+?)$", lower)
        if match:
            name = match.group(1).strip()
            path = os.path.join(os.path.expanduser("~\\Desktop"), name)
            return self.fm.create_folder(path)

        return None

    def _detect_disk_info(self, lower):
        """disk space, storage info"""
        if any(kw in lower for kw in ["disk space", "storage space", "free space",
                                       "drive space", "disk info", "storage info",
                                       "kitni space"]):
            drives = ["C:"]
            for d in ["D:", "E:", "K:"]:
                if os.path.exists(d + "\\"):
                    drives.append(d)

            output = "💾 Disk Space:\n"
            for drive in drives:
                info = self.fm.get_disk_space(drive)
                if isinstance(info, dict):
                    output += f"   {drive} — {info['free']} free / {info['total']} ({info['percent_used']}% used)\n"
            return output
        return None

    def _detect_type_text(self, lower, original):
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
            (r"press\s+tab", "tab"),
            (r"press\s+space", "space"),
            (r"press\s+backspace", "backspace"),
        ]
        for pattern, key in keys:
            if re.search(pattern, text):
                return self.pc.press_key(key)
        return None

    def _detect_window(self, text):
        if any(kw in text for kw in ["minimize", "chhota karo"]):
            return self.pc.minimize_window()
        if any(kw in text for kw in ["maximize", "bara karo", "full screen"]):
            return self.pc.maximize_window()
        if any(kw in text for kw in ["switch window", "alt tab", "next window"]):
            return self.pc.switch_window()
        if any(kw in text for kw in ["show desktop", "desktop dikhao"]):
            return self.pc.show_desktop()
        if any(kw in text for kw in ["close window", "window close"]):
            return self.pc.close_window()
        if "snap left" in text:
            return self.pc.snap_left()
        if "snap right" in text:
            return self.pc.snap_right()
        return None

    def _detect_scroll(self, text):
        if any(kw in text for kw in ["scroll up", "upar scroll"]):
            return self.pc.scroll(5)
        if any(kw in text for kw in ["scroll down", "neeche scroll"]):
            return self.pc.scroll(-5)
        return None

    def _detect_system(self, text):
        if any(kw in text for kw in ["lock screen", "lock computer"]):
            return self.pc.lock_screen()
        if "mouse position" in text:
            return self.pc.get_mouse_position()
        if any(kw in text for kw in ["screen size", "resolution"]):
            return self.pc.get_screen_size()
        if any(kw in text for kw in ["sleep computer", "hibernate"]):
            return self.pc.sleep_computer()

        match = re.search(r"(?:brightness|bright)\s*(\d+)", text)
        if match:
            return self.pc.set_brightness(int(match.group(1)))
        return None

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def is_enabled(self):
        return self.enabled