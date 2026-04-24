"""Markdown text editor with basic highlighting."""
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QFont, QTextOption, QColor
from PyQt6.QtCore import Qt


class MarkdownEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        font = QFont("Consolas", 11)
        font.setFixedPitch(True)
        self.setFont(font)

        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setAcceptRichText(False)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                selection-background-color: #094771;
                border: none;
                padding: 12px;
            }
        """)

        self.setTextColor(QColor("#d4d4d4"))
