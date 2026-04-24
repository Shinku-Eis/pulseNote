"""Settings dialog."""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(500, 400)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Settings"))
