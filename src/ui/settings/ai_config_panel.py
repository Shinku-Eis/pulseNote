"""AI Config dialog."""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel


class AIConfigDialog(QDialog):
    def __init__(self, ai_config_repo, parent=None):
        super().__init__(parent)
        self._ai_config_repo = ai_config_repo
        self.setWindowTitle("AI Settings")
        self.resize(500, 400)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("AI Configuration"))
