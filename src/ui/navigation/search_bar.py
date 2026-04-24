"""Search bar widget."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal

from ...services.search_service import SearchService


class SearchBar(QWidget):

    search_result_selected = pyqtSignal(int)

    def __init__(self, search_service: SearchService, parent=None):
        super().__init__(parent)
        self._search_service = search_service
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._input = QLineEdit()
        self._input.setPlaceholderText("Search notes...")
        self._results = QListWidget()
        self._results.setSpacing(2)
        layout.addWidget(self._input)
        layout.addWidget(self._results)

    def _connect_signals(self):
        self._input.textChanged.connect(self._on_search)
        self._results.itemClicked.connect(self._on_result_clicked)

    def _on_search(self, text: str):
        self._results.clear()
        if len(text.strip()) >= 2:
            results = self._search_service.search(text)
            for r in results:
                item = QListWidgetItem(r["title"])
                item.setData(Qt.ItemDataRole.UserRole, r["id"])
                item.setToolTip(r.get("preview", ""))
                self._results.addItem(item)

    def _on_result_clicked(self, item: QListWidgetItem):
        note_id = item.data(Qt.ItemDataRole.UserRole)
        self.search_result_selected.emit(note_id)
