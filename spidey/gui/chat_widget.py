"""
Spidey GUI — Chat Widget (Message Bubbles)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont


class ChatBubble(QWidget):
    """Single chat message bubble"""

    def __init__(self, message, is_user=True, sender_name="You", parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)

        # Sender name
        name_label = QLabel(sender_name)
        name_label.setObjectName("userName" if is_user else "botName")

        if is_user:
            name_label.setAlignment(Qt.AlignRight)
        else:
            name_label.setAlignment(Qt.AlignLeft)

        layout.addWidget(name_label)

        # Message bubble
        bubble = QLabel(message)
        bubble.setObjectName("userBubble" if is_user else "botBubble")
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)
        bubble.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        # Alignment
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)

        if is_user:
            h_layout.addStretch()
            h_layout.addWidget(bubble)
        else:
            h_layout.addWidget(bubble)
            h_layout.addStretch()

        layout.addLayout(h_layout)


class ChatWidget(QWidget):
    """Chat area with scrollable message bubbles"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("chatArea")

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("chatScroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Container for messages
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setAlignment(Qt.AlignTop)
        self.messages_layout.setSpacing(5)
        self.messages_layout.setContentsMargins(10, 10, 10, 10)

        # Add stretch at bottom
        self.messages_layout.addStretch()

        self.scroll_area.setWidget(self.messages_container)
        main_layout.addWidget(self.scroll_area)

        # Welcome message
        self.add_bot_message("Hey! I'm Spidey AI 🕷️\nHow can I help you today?")

    def add_user_message(self, message, username="You"):
        """Add a user message bubble"""
        # Remove bottom stretch
        stretch = self.messages_layout.takeAt(self.messages_layout.count() - 1)

        bubble = ChatBubble(message, is_user=True, sender_name=username)
        self.messages_layout.addWidget(bubble)

        # Add stretch back
        self.messages_layout.addStretch()

        # Scroll to bottom
        QTimer.singleShot(100, self._scroll_to_bottom)

    def add_bot_message(self, message, bot_name="🕷️ Spidey"):
        """Add a bot message bubble"""
        # Remove bottom stretch
        stretch = self.messages_layout.takeAt(self.messages_layout.count() - 1)

        bubble = ChatBubble(message, is_user=False, sender_name=bot_name)
        self.messages_layout.addWidget(bubble)

        # Add stretch back
        self.messages_layout.addStretch()

        # Scroll to bottom
        QTimer.singleShot(100, self._scroll_to_bottom)

    def add_loading(self):
        """Add typing indicator"""
        stretch = self.messages_layout.takeAt(self.messages_layout.count() - 1)

        self.loading_label = QLabel("🕷️ Spidey is thinking...")
        self.loading_label.setObjectName("loadingLabel")
        self.messages_layout.addWidget(self.loading_label)

        self.messages_layout.addStretch()
        QTimer.singleShot(100, self._scroll_to_bottom)

    def remove_loading(self):
        """Remove typing indicator"""
        if hasattr(self, 'loading_label'):
            self.loading_label.deleteLater()
            del self.loading_label

    def clear_chat(self):
        """Clear all messages"""
        while self.messages_layout.count() > 1:
            item = self.messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.add_bot_message("Chat cleared! Fresh start 🕷️")

    def _scroll_to_bottom(self):
        """Scroll to the bottom of chat"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())