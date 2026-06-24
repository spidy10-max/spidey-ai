"""
Spidey AI — Computer Control (Enhanced!)
Open apps, screenshots to K drive, screen recorder, browser control!
"""
import pyautogui
import subprocess
import os
import time
import threading
from spidey.config import DATA_DIR
from spidey.logger import app_logger, log_event, log_error


# Safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# Screenshot folder — K drive
SCREENSHOTS_DIR = "K:\\SpideyScreenshots"
if not os.path.exists("K:\\"):
    SCREENSHOTS_DIR = os.path.join(DATA_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Recordings folder — K drive
RECORDINGS_DIR = "K:\\SpideyRecordings"
if not os.path.exists("K:\\"):
    RECORDINGS_DIR = os.path.join(DATA_DIR, "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)


class ComputerControl:
    """Enhanced desktop automation"""

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self._recording = False
        self._record_process = None
        app_logger.info(f"ComputerControl — Screen: {self.screen_width}x{self.screen_height}")

    # ============================================================
    #  APP LAUNCHER (Enhanced!)
    # ============================================================

    def open_app(self, app_name):
        """Open application — enhanced with multiple methods!"""
        app_name = app_name.lower().strip()

        # Method 1: Direct commands
        direct_commands = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "paint": "mspaint.exe",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "terminal": "wt.exe",
            "powershell": "powershell.exe",
            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",
            "files": "explorer.exe",
            "task manager": "taskmgr.exe",
            "snipping tool": "snippingtool.exe",
            "wordpad": "wordpad.exe",
            "control panel": "control.exe",
            "device manager": "devmgmt.msc",
            "disk management": "diskmgmt.msc",
            "registry": "regedit.exe",
            "system info": "msinfo32.exe",
        }

        # Method 2: Start menu search (for apps like Chrome, VS Code)
        start_commands = {
            "chrome": "chrome",
            "google chrome": "chrome",
            "google": "chrome",
            "browser": "chrome",
            "firefox": "firefox",
            "edge": "msedge",
            "microsoft edge": "msedge",
            "brave": "brave",
            "opera": "opera",
            "vscode": "code",
            "vs code": "code",
            "visual studio code": "code",
            "visual studio": "devenv",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "outlook": "outlook",
            "onenote": "onenote",
            "teams": "teams",
            "spotify": "spotify",
            "discord": "discord",
            "telegram": "telegram",
            "whatsapp": "whatsapp",
            "zoom": "zoom",
            "obs": "obs64",
            "obs studio": "obs64",
            "vlc": "vlc",
            "media player": "wmplayer",
            "photos": "ms-photos:",
            "camera": "microsoft.windows.camera:",
            "store": "ms-windows-store:",
            "maps": "bingmaps:",
            "weather": "bingweather:",
            "clock": "ms-clock:",
            "alarm": "ms-clock:",
        }

        # Method 3: Settings pages
        settings_commands = {
            "settings": "ms-settings:",
            "wifi": "ms-settings:network-wifi",
            "bluetooth": "ms-settings:bluetooth",
            "display": "ms-settings:display",
            "sound": "ms-settings:sound",
            "notifications": "ms-settings:notifications",
            "battery": "ms-settings:batterysaver",
            "storage": "ms-settings:storagesense",
            "about": "ms-settings:about",
            "update": "ms-settings:windowsupdate",
            "personalization": "ms-settings:personalization",
            "wallpaper": "ms-settings:personalization-background",
            "mouse settings": "ms-settings:mousetouchpad",
            "keyboard settings": "ms-settings:typing",
            "apps": "ms-settings:appsfeatures",
            "default apps": "ms-settings:defaultapps",
        }

        try:
            # Check direct commands first
            if app_name in direct_commands:
                subprocess.Popen(direct_commands[app_name], shell=True)
                log_event("App opened (direct)", app_name)
                return f"✅ Opened {app_name}"

            # Check start commands
            if app_name in start_commands:
                cmd = start_commands[app_name]
                if cmd.endswith(":"):
                    # Windows URI scheme
                    os.system(f'start "" "{cmd}"')
                else:
                    # Try direct first
                    try:
                        subprocess.Popen(cmd, shell=True)
                    except Exception:
                        # Try start menu search
                        os.system(f'start "" "{cmd}"')

                log_event("App opened (start)", app_name)
                return f"✅ Opened {app_name}"

            # Check settings
            if app_name in settings_commands:
                os.system(f'start "" "{settings_commands[app_name]}"')
                log_event("Settings opened", app_name)
                return f"✅ Opened {app_name} settings"

            # Try generic — search in common paths
            common_paths = [
                os.path.expandvars(r"%ProgramFiles%"),
                os.path.expandvars(r"%ProgramFiles(x86)%"),
                os.path.expandvars(r"%LocalAppData%"),
                os.path.expandvars(r"%AppData%"),
            ]

            for path in common_paths:
                for root, dirs, files in os.walk(path):
                    for f in files:
                        if app_name in f.lower() and f.endswith(".exe"):
                            full_path = os.path.join(root, f)
                            subprocess.Popen(full_path)
                            log_event("App opened (search)", full_path)
                            return f"✅ Opened {f}"
                    # Only check first 2 levels
                    if root.count(os.sep) - path.count(os.sep) > 2:
                        break

            # Last try — just run it
            subprocess.Popen(app_name, shell=True)
            log_event("App opened (generic)", app_name)
            return f"✅ Opened {app_name}"

        except Exception as e:
            log_error(str(e), f"open_app({app_name})")
            return f"❌ Could not open {app_name}: {e}"

    def close_app(self, app_name):
        """Close application"""
        app_name = app_name.lower().strip()

        process_map = {
            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",
            "browser": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "notepad": "notepad.exe",
            "calculator": "Calculator.exe",
            "paint": "mspaint.exe",
            "vscode": "Code.exe",
            "vs code": "Code.exe",
            "explorer": "explorer.exe",
            "word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "powerpoint": "POWERPNT.EXE",
            "spotify": "Spotify.exe",
            "discord": "Discord.exe",
            "telegram": "Telegram.exe",
            "vlc": "vlc.exe",
            "obs": "obs64.exe",
            "zoom": "Zoom.exe",
            "teams": "Teams.exe",
        }

        process = process_map.get(app_name, f"{app_name}.exe")

        try:
            os.system(f"taskkill /f /im {process} 2>nul")
            log_event("App closed", app_name)
            return f"✅ Closed {app_name}"
        except Exception as e:
            return f"❌ Could not close {app_name}: {e}"

    # ============================================================
    #  CHROME / BROWSER CONTROL
    # ============================================================

    def open_chrome(self, url=None):
        """Open Chrome specifically — multiple methods!"""
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        ]

        for path in chrome_paths:
            if os.path.exists(path):
                try:
                    if url:
                        subprocess.Popen([path, url])
                    else:
                        subprocess.Popen([path])
                    log_event("Chrome opened", url or "homepage")
                    return f"✅ Chrome opened" + (f" — {url}" if url else "")
                except Exception:
                    continue

        # Fallback: start command
        try:
            if url:
                os.system(f'start chrome "{url}"')
            else:
                os.system('start chrome')
            return f"✅ Chrome opened" + (f" — {url}" if url else "")
        except Exception:
            pass

        # Fallback: default browser
        try:
            import webbrowser
            if url:
                webbrowser.open(url)
            else:
                webbrowser.open("https://www.google.com")
            return "✅ Browser opened"
        except Exception as e:
            return f"❌ Could not open Chrome: {e}"

    def chrome_new_tab(self, url=None):
        """Open new tab in Chrome"""
        try:
            if url:
                os.system(f'start chrome "{url}"')
                return f"✅ New tab: {url}"
            else:
                pyautogui.hotkey('ctrl', 't')
                return "✅ New tab opened"
        except Exception as e:
            return f"❌ Error: {e}"

    def chrome_search(self, query):
        """Search in Chrome"""
        try:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            self.open_chrome(url)
            return f"✅ Searching: {query}"
        except Exception as e:
            return f"❌ Search error: {e}"

    # ============================================================
    #  SCREENSHOT (Save to K drive!)
    # ============================================================

    def take_screenshot(self, filename=None):
        """Take screenshot — saves to K drive!"""
        try:
            if not filename:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"

            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)

            log_event("Screenshot", filepath)
            return f"✅ Screenshot saved: {filepath}"
        except Exception as e:
            return f"❌ Screenshot failed: {e}"

    def take_region_screenshot(self, x, y, width, height, filename=None):
        """Screenshot of specific region"""
        try:
            if not filename:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"region_{timestamp}.png"

            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            screenshot.save(filepath)

            return f"✅ Region screenshot saved: {filepath}"
        except Exception as e:
            return f"❌ Error: {e}"

    # ============================================================
    #  SCREEN RECORDER! 🎬
    # ============================================================

    def start_recording(self, filename=None, duration=None):
        """
        Start screen recording using ffmpeg!
        Saves to K drive!
        """
        if self._recording:
            return "⚠️ Already recording! Say 'stop recording' to stop."

        try:
            if not filename:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"recording_{timestamp}.mp4"

            filepath = os.path.join(RECORDINGS_DIR, filename)

            # FFmpeg screen recording command (Windows)
            cmd = [
                "ffmpeg",
                "-f", "gdigrab",
                "-framerate", "15",
                "-i", "desktop",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                filepath
            ]

            if duration:
                cmd.insert(-1, "-t")
                cmd.insert(-1, str(duration))

            # Start recording in background
            self._record_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self._recording = True
            self._recording_file = filepath

            log_event("Recording started", filepath)

            if duration:
                # Auto-stop after duration
                def auto_stop():
                    time.sleep(duration + 1)
                    if self._recording:
                        self.stop_recording()

                thread = threading.Thread(target=auto_stop, daemon=True)
                thread.start()
                return f"✅ Recording started! ({duration} seconds) → {filepath}"
            else:
                return f"✅ Recording started! Say 'stop recording' to stop. → {filepath}"

        except FileNotFoundError:
            return "❌ FFmpeg not found! Install FFmpeg for screen recording."
        except Exception as e:
            self._recording = False
            log_error(str(e), "start_recording")
            return f"❌ Recording error: {e}"

    def stop_recording(self):
        """Stop screen recording"""
        if not self._recording:
            return "⚠️ Not recording!"

        try:
            if self._record_process:
                # Send 'q' to ffmpeg to gracefully stop
                self._record_process.stdin.write(b'q')
                self._record_process.stdin.flush()

                # Wait for process to finish
                try:
                    self._record_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self._record_process.kill()

                self._record_process = None

            self._recording = False
            filepath = getattr(self, '_recording_file', 'unknown')

            log_event("Recording stopped", filepath)
            return f"✅ Recording saved: {filepath}"

        except Exception as e:
            self._recording = False
            self._record_process = None
            log_error(str(e), "stop_recording")
            return f"❌ Stop error: {e}"

    def is_recording(self):
        """Check if recording"""
        return self._recording

    def record_for(self, seconds):
        """Record screen for fixed duration"""
        return self.start_recording(duration=seconds)

    # ============================================================
    #  MOUSE CONTROL
    # ============================================================

    def move_mouse(self, x, y):
        try:
            pyautogui.moveTo(x, y, duration=0.5)
            return f"✅ Mouse → ({x}, {y})"
        except Exception as e:
            return f"❌ Error: {e}"

    def click(self, x=None, y=None):
        try:
            if x and y:
                pyautogui.click(x, y)
            else:
                pyautogui.click()
            return "✅ Clicked"
        except Exception as e:
            return f"❌ Error: {e}"

    def double_click(self, x=None, y=None):
        try:
            if x and y:
                pyautogui.doubleClick(x, y)
            else:
                pyautogui.doubleClick()
            return "✅ Double clicked"
        except Exception as e:
            return f"❌ Error: {e}"

    def right_click(self, x=None, y=None):
        try:
            if x and y:
                pyautogui.rightClick(x, y)
            else:
                pyautogui.rightClick()
            return "✅ Right clicked"
        except Exception as e:
            return f"❌ Error: {e}"

    def scroll(self, amount):
        """Scroll up (+) or down (-)"""
        try:
            pyautogui.scroll(amount)
            direction = "up" if amount > 0 else "down"
            return f"✅ Scrolled {direction}"
        except Exception as e:
            return f"❌ Error: {e}"

    def get_mouse_position(self):
        x, y = pyautogui.position()
        return f"Mouse at ({x}, {y})"

    # ============================================================
    #  KEYBOARD CONTROL
    # ============================================================

    def type_text(self, text, interval=0.02):
        try:
            pyautogui.typewrite(text, interval=interval)
            return f"✅ Typed: {text[:30]}..."
        except Exception:
            try:
                import pyperclip
                pyperclip.copy(text)
                pyautogui.hotkey('ctrl', 'v')
                return f"✅ Typed: {text[:30]}..."
            except Exception as e:
                return f"❌ Error: {e}"

    def press_key(self, key):
        try:
            pyautogui.press(key)
            return f"✅ Pressed: {key}"
        except Exception as e:
            return f"❌ Error: {e}"

    def hotkey(self, *keys):
        try:
            pyautogui.hotkey(*keys)
            return f"✅ Hotkey: {'+'.join(keys)}"
        except Exception as e:
            return f"❌ Error: {e}"

    def press_enter(self):
        pyautogui.press('enter')
        return "✅ Enter"

    def press_escape(self):
        pyautogui.press('escape')
        return "✅ Escape"

    # ============================================================
    #  FILE OPERATIONS
    # ============================================================

    def open_folder(self, path):
        try:
            if os.path.exists(path):
                os.startfile(path)
                return f"✅ Opened: {path}"
            return f"❌ Not found: {path}"
        except Exception as e:
            return f"❌ Error: {e}"

    def open_file(self, filepath):
        try:
            if os.path.exists(filepath):
                os.startfile(filepath)
                return f"✅ Opened: {filepath}"
            return f"❌ Not found: {filepath}"
        except Exception as e:
            return f"❌ Error: {e}"

    def search_files(self, directory, pattern, extension=None):
        try:
            results = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if pattern.lower() in file.lower():
                        if extension and not file.endswith(extension):
                            continue
                        results.append(os.path.join(root, file))
                        if len(results) >= 20:
                            return results
                if root.count(os.sep) - directory.count(os.sep) > 3:
                    break
            return results
        except Exception as e:
            log_error(str(e), "search_files")
            return []

    # ============================================================
    #  WINDOW CONTROL
    # ============================================================

    def minimize_window(self):
        """Minimize current window"""
        try:
            pyautogui.hotkey('win', 'down')
            return "✅ Window minimized"
        except Exception as e:
            return f"❌ Error: {e}"

    def maximize_window(self):
        """Maximize current window"""
        try:
            pyautogui.hotkey('win', 'up')
            return "✅ Window maximized"
        except Exception as e:
            return f"❌ Error: {e}"

    def switch_window(self):
        """Alt+Tab"""
        try:
            pyautogui.hotkey('alt', 'tab')
            return "✅ Switched window"
        except Exception as e:
            return f"❌ Error: {e}"

    def show_desktop(self):
        """Show desktop"""
        try:
            pyautogui.hotkey('win', 'd')
            return "✅ Desktop shown"
        except Exception as e:
            return f"❌ Error: {e}"

    def close_window(self):
        """Close current window"""
        try:
            pyautogui.hotkey('alt', 'F4')
            return "✅ Window closed"
        except Exception as e:
            return f"❌ Error: {e}"

    def snap_left(self):
        """Snap window to left"""
        try:
            pyautogui.hotkey('win', 'left')
            return "✅ Snapped left"
        except Exception as e:
            return f"❌ Error: {e}"

    def snap_right(self):
        """Snap window to right"""
        try:
            pyautogui.hotkey('win', 'right')
            return "✅ Snapped right"
        except Exception as e:
            return f"❌ Error: {e}"

    # ============================================================
    #  SYSTEM
    # ============================================================

    def get_screen_size(self):
        return f"Screen: {self.screen_width}x{self.screen_height}"

    def lock_screen(self):
        try:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "✅ Screen locked"
        except Exception as e:
            return f"❌ Error: {e}"

    def open_url(self, url):
        try:
            import webbrowser
            webbrowser.open(url)
            return f"✅ Opened: {url}"
        except Exception as e:
            return f"❌ Error: {e}"

    def sleep_computer(self):
        """Put computer to sleep"""
        try:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "✅ Going to sleep..."
        except Exception as e:
            return f"❌ Error: {e}"

    def empty_recycle_bin(self):
        """Empty recycle bin"""
        try:
            os.system("rd /s /q C:\\$Recycle.Bin 2>nul")
            return "✅ Recycle bin emptied"
        except Exception as e:
            return f"❌ Error: {e}"

    # ============================================================
    #  BRIGHTNESS (Windows)
    # ============================================================

    def set_brightness(self, level):
        """Set screen brightness (0-100)"""
        try:
            os.system(f'powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})')
            return f"✅ Brightness: {level}%"
        except Exception as e:
            return f"❌ Error: {e}"

    def get_available_commands(self):
        return {
            "Apps": ["open_app", "close_app", "open_chrome"],
            "Browser": ["chrome_new_tab", "chrome_search"],
            "Screenshot": ["take_screenshot", "take_region_screenshot"],
            "Recording": ["start_recording", "stop_recording", "record_for"],
            "Mouse": ["move_mouse", "click", "double_click", "right_click", "scroll"],
            "Keyboard": ["type_text", "press_key", "hotkey"],
            "Window": ["minimize_window", "maximize_window", "switch_window", "show_desktop", "close_window", "snap_left", "snap_right"],
            "Files": ["open_folder", "open_file", "search_files"],
            "System": ["lock_screen", "open_url", "sleep_computer", "set_brightness", "empty_recycle_bin"],
        }