"""
Spidey GUI — Sidebar
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, Signal


class Sidebar(QWidget):
    """Left sidebar with navigation and tools"""

    # Signals
    new_chat_clicked = Signal()
    history_clicked = Signal()
    tools_clicked = Signal()
    settings_clicked = Signal()
    voice_clicked = Signal()
    memory_clicked = Signal()
    stats_clicked = Signal()
    theme_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(250)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title
        title = QLabel("🕷️ SPIDEY AI")
        title.setObjectName("sidebarTitle")
        layout.addWidget(title)

        # === CHAT Section ===
        section1 = QLabel("CHAT")
        section1.setObjectName("sidebarSection")
        layout.addWidget(section1)

        btn_new = QPushButton("🆕  New Chat")
        btn_new.clicked.connect(self.new_chat_clicked.emit)
        layout.addWidget(btn_new)

        btn_history = QPushButton("📋  Chat History")
        btn_history.clicked.connect(self.history_clicked.emit)
        layout.addWidget(btn_history)

        # === TOOLS Section ===
        section2 = QLabel("TOOLS")
        section2.setObjectName("sidebarSection")
        layout.addWidget(section2)

        btn_tools = QPushButton("🔧  Agent Tools")
        btn_tools.clicked.connect(self.tools_clicked.emit)
        layout.addWidget(btn_tools)

        btn_voice = QPushButton("🎤  Voice Mode")
        btn_voice.clicked.connect(self.voice_clicked.emit)
        layout.addWidget(btn_voice)

        btn_memory = QPushButton("🧠  Memories")
        btn_memory.clicked.connect(self.memory_clicked.emit)
        layout.addWidget(btn_memory)

        # === SETTINGS Section ===
        section3 = QLabel("SETTINGS")
        section3.setObjectName("sidebarSection")
        layout.addWidget(section3)

        btn_settings = QPushButton("⚙️  Settings")
        btn_settings.clicked.connect(self.settings_clicked.emit)
        layout.addWidget(btn_settings)

        btn_stats = QPushButton("📊  Statistics")
        btn_stats.clicked.connect(self.stats_clicked.emit)
        layout.addWidget(btn_stats)

        btn_theme = QPushButton("🌙  Toggle Theme")
        btn_theme.clicked.connect(self.theme_clicked.emit)
        layout.addWidget(btn_theme)

        # Stretch
        layout.addStretch()

        # Status
        self.status_label = QLabel("🟢 Online | Groq")
        self.status_label.setObjectName("sidebarSection")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def update_status(self, provider_name, memory_count=0):
        """Update status label"""
        self.status_label.setText(f"🟢 Online | {provider_name} | 🧠 {memory_count}")