"""Main editor widget with markdown source and preview."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QSplitter, QToolBar, QAction
from PyQt6.QtCore import Qt, QTimer

from ...services.note_service import NoteService
from ...services.image_service import ImageService
from ...services.link_service import LinkService
from ..signals import signals
from .markdown_editor import MarkdownEditor
from .preview_panel import PreviewPanel


class EditorWidget(QWidget):
    def __init__(self, note_service: NoteService, image_service: ImageService,
                 link_service: LinkService, parent=None):
        super().__init__(parent)
        self._note_service = note_service
        self._image_service = image_service
        self._link_service = link_service
        self._current_note_id = None
        self._autosave_timer = QTimer()
        self._autosave_timer.setInterval(2000)
        self._autosave_timer.timeout.connect(self._autosave)

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._title_edit = QLineEdit()
        self._title_edit.setPlaceholderText("Note title...")
        self._title_edit.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                font-weight: 600;
                padding: 8px 12px;
                border: none;
                border-bottom: 1px solid #404040;
            }
        """)

        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._editor = MarkdownEditor()
        self._preview = PreviewPanel()
        self._splitter.addWidget(self._editor)
        self._splitter.addWidget(self._preview)
        self._splitter.setStretchFactor(0, 1)
        self._splitter.setStretchFactor(1, 1)

        layout.addWidget(self._title_edit)
        layout.addWidget(self._splitter)

    def _connect_signals(self):
        self._editor.textChanged.connect(self._on_text_changed)
        self._title_edit.textChanged.connect(self._on_title_changed)
        signals.note_created.connect(self.load_note)

    def _on_text_changed(self):
        self._preview.render(self._editor.toPlainText())
        self._autosave_timer.start()

    def _on_title_changed(self):
        self._autosave_timer.start()

    def _autosave(self):
        self._autosave_timer.stop()
        if self._current_note_id:
            self.save_note()

    def load_note(self, note_id: int):
        self._autosave_timer.stop()
        self._current_note_id = note_id
        note = self._note_service.get_by_id(note_id)
        if note:
            self._title_edit.setText(note.title)
            self._editor.setPlainText(note.content)
            self._preview.render(note.content)

    def save_note(self):
        if not self._current_note_id:
            return
        note = self._note_service.get_by_id(self._current_note_id)
        if note:
            note.title = self._title_edit.text() or "Untitled"
            note.content = self._editor.toPlainText()
            self._note_service.update(note)
            signals.note_saved.emit(self._current_note_id)
