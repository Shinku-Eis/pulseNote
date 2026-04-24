"""Tag panel widget."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt

from ...services.tag_service import TagService
from ..signals import signals


class TagPanel(QWidget):
    def __init__(self, tag_service: TagService, parent=None):
        super().__init__(parent)
        self._tag_service = tag_service
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._list = QListWidget()
        self._list.setSpacing(2)
        layout.addWidget(self._list)

    def refresh(self):
        self._list.clear()
        tags = self._tag_service.get_all()
        for tag in tags:
            item = QListWidgetItem(tag.name)
            item.setData(Qt.ItemDataRole.UserRole, tag.id)
            if tag.color:
                item.setForeground(Qt.GlobalColor(tag.color))
            self._list.addItem(item)
