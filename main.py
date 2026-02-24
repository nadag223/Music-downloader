from gui import MediaDownloaderGUI
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QSpinBox,
    QProgressBar, QTextEdit, QFileDialog, QDialog, QScrollArea,
    QFrame, QSizePolicy, QSpacerItem,)

from PyQt6.QtGui import (
    QFont, QColor, QPalette, QPainter, QBrush,
)

import threading
from PyQt6.QtGui import QIcon  # כבר יש לך import חלקי, אבל תוודא שיש QIcon

def main():
    C_BG = "#0A0C12"
    C_SURFACE = "#111520"
    C_CARD = "#161B27"
    C_BORDER = "#1E2535"
    C_ACCENT = "#3B82F6"
    C_ACCENT2 = "#06B6D4"
    C_SUCCESS = "#10B981"
    C_DANGER = "#EF4444"
    C_TEXT = "#E8EEFF"
    C_TEXT_DIM = "#5A6480"
    C_TEXT_MID = "#8B93B0"

    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(C_BG))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(C_TEXT))
    palette.setColor(QPalette.ColorRole.Base, QColor(C_CARD))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(C_SURFACE))
    palette.setColor(QPalette.ColorRole.Text, QColor(C_TEXT))
    palette.setColor(QPalette.ColorRole.Button, QColor(C_CARD))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(C_TEXT))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(C_ACCENT))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
    app.setPalette(palette)

    win = MediaDownloaderGUI()
    win.setWindowIcon(QIcon("logo.ico"))  # <-- כאן מוסיפים את האייקון של החלון
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
