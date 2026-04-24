"""Folder tree widget for navigation."""
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QInputDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction

from ...services.folder_service import FolderService
from ..signals import get_signals


class FolderTree(QTreeWidget):

    folder_selected = pyqtSignal(int)

    def __init__(self, folder_service: FolderService, parent=None):
        super().__init__(parent)
        self._folder_service = folder_service
        self._signals = get_signals()
        self._setup_ui()
        self._connect_signals()
        self.refresh()

    def _setup_ui(self):
        self.setHeaderHidden(True)
        self.setIndentation(16)
        self.setAnimated(True)
        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        self._all_notes_item = QTreeWidgetItem(self, ["All Notes"])
        self._all_notes_item.setData(0, Qt.ItemDataRole.UserRole, None)
        self._all_notes_item.setIcon(0, self.style().standardIcon(
            self.style().StandardPixmap.SP_DirHomeIcon))
        self._all_notes_item.setExpanded(True)

    def _connect_signals(self):
        self.itemClicked.connect(self._on_item_clicked)
        self._signals.folder_changed.connect(self.refresh)
        self._signals.note_list_refresh.connect(self.refresh)

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        folder_id = item.data(0, Qt.ItemDataRole.UserRole)
        self._signals.folder_selected.emit(folder_id)

    def refresh(self):
        expanded = set()
        for i in range(self._all_notes_item.childCount()):
            child = self._all_notes_item.child(i)
            self._save_expanded(child, expanded)

        self._all_notes_item.takeChildren()

        tree_data = self._folder_service.build_tree()
        self._add_nodes(self._all_notes_item, tree_data, expanded)

        self.setCurrentItem(self._all_notes_item)
        self._signals.folder_selected.emit(None)

    def _save_expanded(self, item: QTreeWidgetItem, expanded: set):
        if item.isExpanded():
            expanded.add(item.text(0))
        for i in range(item.childCount()):
            self._save_expanded(item.child(i), expanded)

    def _add_nodes(self, parent_item: QTreeWidgetItem, nodes: list[dict], expanded: set):
        for node in nodes:
            folder = node["folder"]
            item = QTreeWidgetItem(parent_item, [folder.name])
            item.setData(0, Qt.ItemDataRole.UserRole, folder.id)
            item.setIcon(0, self.style().standardIcon(
                self.style().StandardPixmap.SP_DirIcon))
            if folder.name in expanded:
                item.setExpanded(True)
            self._add_nodes(item, node["children"], expanded)

    def _show_context_menu(self, pos):
        item = self.itemAt(pos)
        menu = QMenu(self)

        new_folder_action = QAction("New Folder", self)
        new_folder_action.triggered.connect(self._on_new_folder)
        menu.addAction(new_folder_action)

        if item and item is not self._all_notes_item:
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self._on_delete(item))
            menu.addAction(delete_action)

        menu.exec(self.mapToGlobal(pos))

    def _on_new_folder(self):
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and name.strip():
            parent_id = self.get_selected_folder_id()
            self._folder_service.create(name.strip(), parent_id)
            self._signals.folder_changed.emit()
            self._signals.status_message.emit(f'Folder "{name}" created', 3000)

    def _on_delete(self, item: QTreeWidgetItem):
        folder_id = item.data(0, Qt.ItemDataRole.UserRole)
        if folder_id:
            self._folder_service.delete(folder_id)
            self._signals.folder_changed.emit()
            self._signals.status_message.emit("Folder deleted", 3000)

    def get_selected_folder_id(self) -> int | None:
        item = self.currentItem()
        if item:
            return item.data(0, Qt.ItemDataRole.UserRole)
        return None
