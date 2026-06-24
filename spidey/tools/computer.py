"""
Spidey AI — Computer Control
Desktop automation using PyAutoGUI
Open apps, type text, take screenshots, move mouse!
"""
import pyautogui
import subprocess
import os
import time
from spidey.config import DATA_DIR
from spidey.logger import app_logger, log_event, log_error


# Safety settings
pyautogui.FAILSAFE = True  # Move mouse to corner = emergency stop
pyautogui.PAUSE = 0.5  # Pause between actions

SCREENSHOTS_DIR = os.path.join(DATA_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


class ComputerControl:
    """Desktop automation — open apps, type, click, screenshot"""

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        app_logger.info(f"ComputerControl ready — Screen: {self.screen_width}x{self.screen_height}")

    # ============================================================
    #  APP LAUNCHER
    # ============================================================

    def open_app(self, app_name):
        """
        Open an application by name

        Supported: chrome, notepad, calculator, vscode,
                   explorer, cmd, settings, paint, etc.
        """
        app_name = app_name.lower().strip()

        # Windows app commands
        apps = {
            "chrome": "chrome",
            "google chrome": "chrome",
            "browser": "chrome",
            "notepad": "notepad",
            "calculator": "calc",
            "calc": "calc",
            "paint": "mspaint",
            "cmd": "cmd",
            "command prompt": "cmd",
            "terminal": "cmd",
            "powershell": "powershell",
            "explorer": "explorer",
            "file explorer": "explorer",
            "files": "explorer",
            "settings": "ms-settings:",
            "task manager": "taskmgr",
            "vscode": "code",
            "vs code": "code",
            "visual studio code": "code",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "spotify": "spotify",
            "discord": "discord",
            "snipping tool": "snippingtool",
            "screenshot": "snippingtool",
        }

        if app_name in apps:
            cmd = apps[app_name]
        else:
            cmd = app_name

        try:
            if cmd.startswith("ms-settings"):
                os.system(f"start {cmd}")
            else:
                subprocess.Popen(cmd, shell=True)

            log_event("App opened", app_name)
            return f"✅ Opened {app_name}"

        except Exception as e:
            log_error(str(e), f"open_app({app_name})")
            return f"❌ Could not open {app_name}: {e}"

    def close_app(self, app_name):
        """Close an application"""
        app_name = app_name.lower().strip()

        process_names = {
            "chrome": "chrome.exe",
            "notepad": "notepad.exe",
            "calculator": "Calculator.exe",
            "paint": "mspaint.exe",
            "vscode": "Code.exe",
            "vs code": "Code.exe",
            "explorer": "explorer.exe",
            "word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "spotify": "Spotify.exe",
            "discord": "Discord.exe",
        }

        process = process_names.get(app_name, f"{app_name}.exe")

        try:
            os.system(f"taskkill /f /im {process}")
            log_event("App closed", app_name)
            return f"✅ Closed {app_name}"
        except Exception as e:
            log_error(str(e), f"close_app({app_name})")
            return f"❌ Could not close {app_name}: {e}"

    # ============================================================
    #  SCREENSHOT
    # ============================================================

    def take_screenshot(self, filename=None):
        """Take a screenshot and save"""
        try:
            if not filename:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"

            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)

            log_event("Screenshot taken", filepath)
            return f"✅ Screenshot saved: {filepath}"

        except Exception as e:
            log_error(str(e), "take_screenshot")
            return f"❌ Screenshot failed: {e}"

    # ============================================================
    #  MOUSE CONTROL
    # ============================================================

    def move_mouse(self, x, y):
        """Move mouse to position"""
        try:
            pyautogui.moveTo(x, y, duration=0.5)
            return f"✅ Mouse moved to ({x}, {y})"
        except Exception as e:
            return f"❌ Mouse error: {e}"

    def click(self, x=None, y=None):
        """Click at position (or current position)"""
        try:
            if x and y:
                pyautogui.click(x, y)
                return f"✅ Clicked at ({x}, {y})"
            else:
                pyautogui.click()
                return "✅ Clicked"
        except Exception as e:
            return f"❌ Click error: {e}"

    def double_click(self, x=None, y=None):
        """Double click"""
        try:
            if x and y:
                pyautogui.doubleClick(x, y)
            else:
                pyautogui.doubleClick()
            return "✅ Double clicked"
        except Exception as e:
            return f"❌ Error: {e}"

    def right_click(self, x=None, y=None):
        """Right click"""
        try:
            if x and y:
                pyautogui.rightClick(x, y)
            else:
                pyautogui.rightClick()
            return "✅ Right clicked"
        except Exception as e:
            return f"❌ Error: {e}"

    def get_mouse_position(self):
        """Get current mouse position"""
        x, y = pyautogui.position()
        return f"Mouse at ({x}, {y})"

    # ============================================================
    #  KEYBOARD CONTROL
    # ============================================================

    def type_text(self, text, interval=0.02):
        """Type text"""
        try:
            pyautogui.typewrite(text, interval=interval)
            return f"✅ Typed: {text[:30]}..."
        except Exception as e:
            # For non-ASCII characters
            try:
                import pyperclip
                pyperclip.copy(text)
                pyautogui.hotkey('ctrl', 'v')
                return f"✅ Typed (paste): {text[:30]}..."
            except Exception as e2:
                return f"❌ Type error: {e2}"

    def press_key(self, key):
        """Press a single key"""
        try:
            pyautogui.press(key)
            return f"✅ Pressed: {key}"
        except Exception as e:
            return f"❌ Key error: {e}"

    def hotkey(self, *keys):
        """Press key combination (e.g., ctrl+c)"""
        try:
            pyautogui.hotkey(*keys)
            return f"✅ Hotkey: {'+'.join(keys)}"
        except Exception as e:
            return f"❌ Hotkey error: {e}"

    def press_enter(self):
        """Press Enter"""
        pyautogui.press('enter')
        return "✅ Enter pressed"

    def press_escape(self):
        """Press Escape"""
        pyautogui.press('escape')
        return "✅ Escape pressed"

    # ============================================================
    #  FILE OPERATIONS
    # ============================================================

    def open_folder(self, path):
        """Open a folder in Explorer"""
        try:
            if os.path.exists(path):
                os.startfile(path)
                log_event("Folder opened", path)
                return f"✅ Opened: {path}"
            else:
                return f"❌ Path not found: {path}"
        except Exception as e:
            return f"❌ Error: {e}"

    def open_file(self, filepath):
        """Open a file with default app"""
        try:
            if os.path.exists(filepath):
                os.startfile(filepath)
                log_event("File opened", filepath)
                return f"✅ Opened: {filepath}"
            else:
                return f"❌ File not found: {filepath}"
        except Exception as e:
            return f"❌ Error: {e}"

    def search_files(self, directory, pattern, extension=None):
        """Search files by name pattern"""
        try:
            results = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if pattern.lower() in file.lower():
                        if extension and not file.endswith(extension):
                            continue
                        filepath = os.path.join(root, file)
                        results.append(filepath)
                        if len(results) >= 20:
                            break
                if len(results) >= 20:
                    break

            return results

        except Exception as e:
            log_error(str(e), "search_files")
            return []

    # ============================================================
    #  SCREEN INFO
    # ============================================================

    def get_screen_size(self):
        """Get screen resolution"""
        return f"Screen: {self.screen_width}x{self.screen_height}"

    # ============================================================
    #  SYSTEM COMMANDS
    # ============================================================

    def set_volume(self, level):
        """Set system volume (0-100) — Windows only"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            return f"✅ Volume: {level}%"
        except Exception:
            # Fallback — use nircmd if available
            try:
                vol = int(65535 * level / 100)
                os.system(f"nircmd setsysvolume {vol}")
                return f"✅ Volume: {level}%"
            except Exception as e:
                return f"❌ Volume error: {e}"

    def lock_screen(self):
        """Lock the computer"""
        try:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "✅ Screen locked"
        except Exception as e:
            return f"❌ Lock error: {e}"

    def open_url(self, url):
        """Open URL in default browser"""
        try:
            import webbrowser
            webbrowser.open(url)
            log_event("URL opened", url)
            return f"✅ Opened: {url}"
        except Exception as e:
            return f"❌ URL error: {e}"

    def get_available_commands(self):
        """List all available commands"""
        return {
            "Apps": ["open_app", "close_app"],
            "Screenshot": ["take_screenshot"],
            "Mouse": ["move_mouse", "click", "double_click", "right_click", "get_mouse_position"],
            "Keyboard": ["type_text", "press_key", "hotkey", "press_enter", "press_escape"],
            "Files": ["open_folder", "open_file", "search_files"],
            "System": ["set_volume", "lock_screen", "open_url", "get_screen_size"],
        }