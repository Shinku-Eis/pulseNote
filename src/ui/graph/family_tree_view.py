"""Family Tree widget."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class FamilyTreeWidget(QWidget):
    def __init__(self, topic_service, parent=None):
        super().__init__(parent)
        self._topic_service = topic_service
        layout = QVBoxLayout(self)
        label = QLabel("Family Tree View")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
