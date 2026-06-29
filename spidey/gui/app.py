"""
Spidey GUI — App Launcher
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from spidey.gui.main_window import MainWindow


def launch_gui():
    """Launch Spidey AI GUI"""
    app = QApplication(sys.argv)

    # Set app font
    font = QFont("Segoe UI", 11)
    app.setFont(font)

    # Create and show window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    launch_gui()