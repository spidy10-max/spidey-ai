"""
🖥️ Spidey Tools Module

Contains:
- computer.py      — Desktop automation (PyAutoGUI)
- file_manager.py  — Advanced file search & management
- system_info.py   — System information (battery, wifi, etc.)
- tool_connector.py — AI to tools bridge (NLP command detection)

Supported Commands:
- Apps: open/close any application
- Browser: Chrome, search, new tab, URLs
- Screenshot: Full screen capture (K drive)
- Recording: Screen recording with FFmpeg
- Files: Search by name, type, recent, large
- System: Battery, WiFi, IP, uptime, running apps
- Window: Minimize, maximize, snap, switch
- Keyboard: Hotkeys, type text, press keys
"""

from spidey.tools.tool_connector import ToolConnector
from spidey.tools.computer import ComputerControl
from spidey.tools.file_manager import FileManager
from spidey.tools.system_info import SystemInfo

__all__ = [
    "ToolConnector",
    "ComputerControl",
    "FileManager",
    "SystemInfo"
]