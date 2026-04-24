"""Knowledge Graph widget."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class KnowledgeGraphWidget(QWidget):
    def __init__(self, link_service, parent=None):
        super().__init__(parent)
        self._link_service = link_service
        layout = QVBoxLayout(self)
        label = QLabel("Knowledge Graph View")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
