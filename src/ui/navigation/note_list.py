"""Note list widget."""
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QMenu
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction

from ...services.note_service import NoteService
from ..signals import signals


class NoteList(QListWidget):

    note_selected = pyqtSignal(int)

    def __init__(self, note_service: NoteService, parent=None):
        super().__init__(parent)
        self._note_service = note_service
        self._current_folder_id = None
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.setSpacing(2)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _connect_signals(self):
        self.itemClicked.connect(self._on_item_clicked)
        signals.folder_selected.connect(self.load_folder)
        signals.note_created.connect(lambda _: self.refresh())
        signals.note_deleted.connect(lambda _: self.refresh())
        signals.note_list_refresh.connect(self.refresh)

    def load_folder(self, folder_id: int | None):
        self._current_folder_id = folder_id
        self.refresh()

    def refresh(self):
        self.clear()
        notes = self._note_service.get_by_folder(self._current_folder_id)
        for note in notes:
            item = QListWidgetItem(note.title)
            item.setData(Qt.ItemDataRole.UserRole, note.id)
            item.setToolTip(note.preview)
            self.addItem(item)

    def _on_item_clicked(self, item: QListWidgetItem):
        note_id = item.data(Qt.ItemDataRole.UserRole)
        self.note_selected.emit(note_id)
        signals.note_selected.emit(note_id)

    def _show_context_menu(self, pos):
        item = self.itemAt(pos)
        menu = QMenu(self)

        if item:
            delete_action = QAction("Delete Note", self)
            delete_action.triggered.connect(lambda: self._on_delete(item))
            menu.addAction(delete_action)

        menu.exec(self.mapToGlobal(pos))

    def _on_delete(self, item: QListWidgetItem):
        note_id = item.data(Qt.ItemDataRole.UserRole)
        self._note_service.delete(note_id)
        signals.note_deleted.emit(note_id)
        signals.status_message.emit("Note deleted", 3000)
