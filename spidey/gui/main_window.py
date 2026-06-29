"""
Spidey GUI — Main Window
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

from spidey.gui.chat_widget import ChatWidget
from spidey.gui.sidebar import Sidebar
from spidey.gui.styles import DARK_THEME
from spidey.brain.chat import SpideyBrain
from spidey.config import settings


class AIWorker(QThread):
    """Background thread for AI responses"""
    response_ready = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, brain, message):
        super().__init__()
        self.brain = brain
        self.message = message

    def run(self):
        try:
            response = self.brain.chat(self.message)
            self.response_ready.emit(response)
        except Exception as e:
            self.error_occurred.emit(str(e))


class AgentWorker(QThread):
    """Background thread for Agent tasks"""
    response_ready = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, brain, task):
        super().__init__()
        self.brain = brain
        self.task = task

    def run(self):
        try:
            response = self.brain.agent_execute(self.task)
            self.response_ready.emit(response)
        except Exception as e:
            self.error_occurred.emit(str(e))


class MainWindow(QMainWindow):
    """Spidey AI Main Window"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("🕷️ Spidey AI")
        self.setMinimumSize(1000, 650)
        self.resize(1200, 750)

        # Apply dark theme
        self.setStyleSheet(DARK_THEME)

        # Initialize brain
        self.brain = SpideyBrain()
        self.brain.start_new_conversation()
        self.username = settings.get("username", "User")
        self.worker = None

        # Setup UI
        self._setup_ui()

    def _setup_ui(self):
        """Setup the main UI layout"""

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === SIDEBAR ===
        self.sidebar = Sidebar()
        self.sidebar.new_chat_clicked.connect(self._new_chat)
        self.sidebar.history_clicked.connect(self._show_history)
        self.sidebar.tools_clicked.connect(self._show_tools)
        self.sidebar.settings_clicked.connect(self._show_settings)
        self.sidebar.voice_clicked.connect(self._voice_mode)
        self.sidebar.memory_clicked.connect(self._show_memories)
        self.sidebar.stats_clicked.connect(self._show_stats)
        self.sidebar.theme_clicked.connect(self._toggle_theme)
        main_layout.addWidget(self.sidebar)

        # === RIGHT SIDE (Header + Chat + Input) ===
        right_side = QWidget()
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setObjectName("header")
        header_layout = QHBoxLayout(header)

        header_title = QLabel("🕷️ Spidey AI")
        header_title.setObjectName("headerTitle")
        header_layout.addWidget(header_title)

        self.header_subtitle = QLabel(f"AI: {self.brain.get_provider_info()['name']}")
        self.header_subtitle.setObjectName("headerSubtitle")
        header_layout.addWidget(self.header_subtitle)

        header_layout.addStretch()

        btn_clear = QPushButton("🗑️")
        btn_clear.setObjectName("headerButton")
        btn_clear.setToolTip("Clear Chat")
        btn_clear.clicked.connect(self._clear_chat)
        header_layout.addWidget(btn_clear)

        right_layout.addWidget(header)

        # Chat area
        self.chat_widget = ChatWidget()
        right_layout.addWidget(self.chat_widget)

        # Input area
        input_area = QWidget()
        input_area.setObjectName("inputArea")
        input_layout = QHBoxLayout(input_area)
        input_layout.setContentsMargins(15, 10, 15, 10)

        # Voice button
        self.voice_btn = QPushButton("🎤")
        self.voice_btn.setObjectName("voiceButton")
        self.voice_btn.setToolTip("Voice Input")
        self.voice_btn.clicked.connect(self._voice_input)
        input_layout.addWidget(self.voice_btn)

        # Message input
        self.message_input = QLineEdit()
        self.message_input.setObjectName("messageInput")
        self.message_input.setPlaceholderText("Type your message...")
        self.message_input.returnPressed.connect(self._send_message)
        input_layout.addWidget(self.message_input)

        # Send button
        self.send_btn = QPushButton("Send 📤")
        self.send_btn.setObjectName("sendButton")
        self.send_btn.clicked.connect(self._send_message)
        input_layout.addWidget(self.send_btn)

        right_layout.addWidget(input_area)

        # Status bar
        self.status_label = QLabel(f"🟢 Ready | {self.brain.get_provider_name()}")
        self.status_label.setObjectName("statusBar")
        right_layout.addWidget(self.status_label)

        main_layout.addWidget(right_side)

        # Update sidebar status
        memories = self.brain.get_all_memories()
        self.sidebar.update_status(
            self.brain.get_provider_info()['name'],
            len(memories) if memories else 0
        )

    def _send_message(self):
        """Send message to AI"""
        message = self.message_input.text().strip()
        if not message:
            return

        # Show user message
        self.chat_widget.add_user_message(message, self.username)
        self.message_input.clear()

        # Show loading
        self.chat_widget.add_loading()
        self.send_btn.setEnabled(False)
        self.status_label.setText("🔄 Thinking...")

        # Check if agent command
        if message.lower().startswith("agent "):
            task = message[6:].strip()
            self.worker = AgentWorker(self.brain, task)
        else:
            self.worker = AIWorker(self.brain, message)

        self.worker.response_ready.connect(self._on_response)
        self.worker.error_occurred.connect(self._on_error)
        self.worker.start()

    def _on_response(self, response):
        """Handle AI response"""
        self.chat_widget.remove_loading()
        self.chat_widget.add_bot_message(response)
        self.send_btn.setEnabled(True)
        self.status_label.setText(f"🟢 Ready | {self.brain.get_provider_name()}")

    def _on_error(self, error):
        """Handle error"""
        self.chat_widget.remove_loading()
        self.chat_widget.add_bot_message(f"⚠️ Error: {error}")
        self.send_btn.setEnabled(True)
        self.status_label.setText("🔴 Error occurred")

    def _new_chat(self):
        """Start new chat"""
        self.brain.reset()
        self.chat_widget.clear_chat()
        self.status_label.setText("🟢 New chat started")

    def _clear_chat(self):
        """Clear chat display"""
        self.chat_widget.clear_chat()

    def _show_history(self):
        """Show chat history"""
        convs = self.brain.get_all_conversations()
        if convs:
            history_text = "📋 Chat History:\n\n"
            for i, c in enumerate(convs[:10], 1):
                history_text += f"{i}. {c['title'][:40]} ({c['message_count']} msgs)\n"
            self.chat_widget.add_bot_message(history_text)
        else:
            self.chat_widget.add_bot_message("📋 No chat history yet!")

    def _show_tools(self):
        """Show available tools"""
        tools = self.brain.agent_tools()
        self.chat_widget.add_bot_message(tools)

    def _show_settings(self):
        """Show settings"""
        info = self.brain.get_provider_info()
        settings_text = (
            f"⚙️ Settings:\n\n"
            f"AI Provider: {info['name']}\n"
            f"Temperature: {self.brain.temperature}\n"
            f"Max Tokens: {self.brain.max_tokens}\n"
            f"Auto Memory: {'ON' if self.brain.auto_memory_enabled else 'OFF'}\n"
            f"Auto Context: {'ON' if self.brain.auto_context else 'OFF'}"
        )
        self.chat_widget.add_bot_message(settings_text)

    def _voice_mode(self):
        """Toggle voice mode"""
        self.chat_widget.add_bot_message("🎤 Voice mode — use terminal for now!\nRun: python -m spidey.main\nThen type: spidey beta")

    def _voice_input(self):
        """Voice input button"""
        self.chat_widget.add_bot_message("🎤 Voice input coming soon!\nUse terminal: python -m spidey.main → v")

    def _show_memories(self):
        """Show memories"""
        memories = self.brain.get_all_memories()
        if memories:
            text = "🧠 Memories:\n\n"
            for k, v in memories.items():
                text += f"• {k}: {v['value']}\n"
            self.chat_widget.add_bot_message(text)
        else:
            self.chat_widget.add_bot_message("🧠 No memories saved yet!")

    def _show_stats(self):
        """Show statistics"""
        stats = self.brain.get_stats()
        text = (
            f"📊 Statistics:\n\n"
            f"Conversations: {stats.get('total_conversations', 0)}\n"
            f"Messages: {stats.get('total_messages', 0)}\n"
            f"Memories: {stats.get('total_preferences', 0)}\n"
            f"Tools: {'ON' if stats.get('tools_enabled') else 'OFF'}"
        )
        self.chat_widget.add_bot_message(text)

    def _toggle_theme(self):
        """Toggle theme placeholder"""
        self.chat_widget.add_bot_message("🌙 Dark theme active!\n☀️ Light theme coming soon!")

    def closeEvent(self, event):
        """Clean up on close"""
        try:
            self.brain.close()
        except Exception:
            pass
        event.accept()