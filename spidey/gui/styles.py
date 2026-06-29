"""
Spidey GUI — Dark Theme Styles
"""

DARK_THEME = """
QMainWindow {
    background-color: #1a1b2e;
}

QWidget {
    background-color: #1a1b2e;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}

/* Sidebar */
#sidebar {
    background-color: #1e2040;
    border-right: 1px solid #2a2d4a;
    min-width: 250px;
    max-width: 250px;
}

#sidebar QPushButton {
    background-color: #252742;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 15px;
    text-align: left;
    font-size: 13px;
    margin: 2px 8px;
}

#sidebar QPushButton:hover {
    background-color: #7c5cfc;
}

#sidebar QPushButton:pressed {
    background-color: #6b4fe0;
}

#sidebarTitle {
    color: #7c5cfc;
    font-size: 18px;
    font-weight: bold;
    padding: 15px;
}

#sidebarSection {
    color: #8b8fa3;
    font-size: 11px;
    font-weight: bold;
    padding: 10px 15px 5px 15px;
    text-transform: uppercase;
}

/* Chat Area */
#chatArea {
    background-color: #1a1b2e;
    border: none;
}

#chatScroll {
    background-color: #1a1b2e;
    border: none;
}

/* Message Bubbles */
#userBubble {
    background-color: #7c5cfc;
    color: #ffffff;
    border-radius: 15px;
    padding: 12px 18px;
    margin: 5px 10px 5px 60px;
    font-size: 14px;
}

#botBubble {
    background-color: #252742;
    color: #e0e0e0;
    border-radius: 15px;
    padding: 12px 18px;
    margin: 5px 60px 5px 10px;
    font-size: 14px;
}

#botName {
    color: #5ce1e6;
    font-size: 12px;
    font-weight: bold;
    margin-left: 15px;
}

#userName {
    color: #7c5cfc;
    font-size: 12px;
    font-weight: bold;
    margin-right: 15px;
    text-align: right;
}

/* Input Area */
#inputArea {
    background-color: #252742;
    border-top: 1px solid #2a2d4a;
    padding: 10px;
}

#messageInput {
    background-color: #2a2d4a;
    color: #ffffff;
    border: 2px solid #3a3d5a;
    border-radius: 20px;
    padding: 12px 20px;
    font-size: 14px;
}

#messageInput:focus {
    border: 2px solid #7c5cfc;
}

#sendButton {
    background-color: #7c5cfc;
    color: #ffffff;
    border: none;
    border-radius: 20px;
    padding: 12px 25px;
    font-size: 14px;
    font-weight: bold;
    min-width: 80px;
}

#sendButton:hover {
    background-color: #8b6fff;
}

#sendButton:pressed {
    background-color: #6b4fe0;
}

#voiceButton {
    background-color: #5ce1e6;
    color: #1a1b2e;
    border: none;
    border-radius: 20px;
    padding: 12px;
    font-size: 16px;
    min-width: 45px;
    max-width: 45px;
}

#voiceButton:hover {
    background-color: #7aeef2;
}

/* Header */
#header {
    background-color: #1e2040;
    border-bottom: 1px solid #2a2d4a;
    padding: 10px 20px;
    min-height: 50px;
}

#headerTitle {
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
}

#headerSubtitle {
    color: #8b8fa3;
    font-size: 12px;
}

#headerButton {
    background-color: transparent;
    color: #8b8fa3;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    font-size: 18px;
}

#headerButton:hover {
    background-color: #252742;
    color: #ffffff;
}

/* Status Bar */
#statusBar {
    background-color: #1e2040;
    color: #8b8fa3;
    font-size: 11px;
    padding: 5px 15px;
    border-top: 1px solid #2a2d4a;
}

/* Scroll Bars */
QScrollBar:vertical {
    background-color: #1a1b2e;
    width: 8px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #3a3d5a;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #7c5cfc;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    height: 0px;
}

/* Tool Cards */
#toolCard {
    background-color: #252742;
    border-radius: 12px;
    padding: 15px;
    margin: 5px;
}

#toolCardTitle {
    color: #5ce1e6;
    font-size: 14px;
    font-weight: bold;
}

/* Loading */
#loadingLabel {
    color: #7c5cfc;
    font-size: 14px;
}
"""