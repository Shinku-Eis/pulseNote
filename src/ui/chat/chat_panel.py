"""AI Chat panel widget."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class ChatPanel(QWidget):
    def __init__(self, ai_config_repo, note_service, parent=None):
        super().__init__(parent)
        self._ai_config_repo = ai_config_repo
        self._note_service = note_service
        layout = QVBoxLayout(self)
        label = QLabel("AI Chat Panel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
