"""Main window shell with menu, toolbar, status bar, and central layout.
Optimized for FAST startup with lazy loading.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QMenuBar, QMenu, QToolBar, QStatusBar,
    QSplitter, QWidget, QVBoxLayout, QTabWidget, QLabel, QInputDialog
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QAction, QKeySequence

from ..core.database import Database
from ..core.repository import (
    FolderRepository, NoteRepository, TagRepository,
    NoteLinkRepository, KnowledgeTopicRepository,
    TopicConnectionRepository, AIConfigRepository,
    ImageRepository, SettingsRepository, AIProcessingLogRepository
)
from ..core.search_engine import SearchEngine
from ..services.note_service import NoteService
from ..services.folder_service import FolderService
from ..services.image_service import ImageService
from ..services.tag_service import TagService
from ..services.link_service import LinkService
from ..services.search_service import SearchService
from ..services.topic_service import TopicService
from .signals import get_signals
from .navigation.folder_tree import FolderTree
from .navigation.note_list import NoteList
from .navigation.tag_panel import TagPanel
from .navigation.search_bar import SearchBar
from .editor.editor_widget import EditorWidget


class MainWindow(QMainWindow):

    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self._lazy_widgets = {}
        self._signals = get_signals()
        self._init_repos()
        self._init_services()
        self._setup_window()
        self._create_actions()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        self._create_central_layout()
        self._connect_signals()
        QTimer.singleShot(100, self._post_init)

    def _init_repos(self):
        conn = self.db.conn
        self.folder_repo = FolderRepository(conn)
        self.note_repo = NoteRepository(conn)
        self.tag_repo = TagRepository(conn)
        self.link_repo = NoteLinkRepository(conn)
        self.topic_repo = KnowledgeTopicRepository(conn)
        self.topic_conn_repo = TopicConnectionRepository(conn)
        self.ai_config_repo = AIConfigRepository(conn)
        self.image_repo = ImageRepository(conn)
        self.settings_repo = SettingsRepository(conn)
        self.ai_log_repo = AIProcessingLogRepository(conn)
        self.search_engine = SearchEngine(conn)

    def _init_services(self):
        self.folder_service = FolderService(self.folder_repo)
        self.note_service = NoteService(self.note_repo)
        self.image_service = ImageService(self.image_repo)
        self.tag_service = TagService(self.tag_repo, self.note_repo)
        self.link_service = LinkService(self.link_repo, self.note_repo)
        self.search_service = SearchService(self.search_engine)
        self.topic_service = TopicService(self.topic_repo, self.topic_conn_repo)

    def _setup_window(self):
        self.setWindowTitle("PulsarNote - Knowledge Management")
        self.resize(1400, 900)
        self.setMinimumSize(1000, 600)
        screen = self.screen().availableGeometry()
        self.move(
            (screen.width() - 1400) // 2,
            (screen.height() - 900) // 2
        )

    def _create_actions(self):
        self.new_note_action = QAction("&New Note", self)
        self.new_note_action.setShortcut(QKeySequence("Ctrl+N"))
        self.new_folder_action = QAction("New &Folder", self)
        self.new_folder_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        self.export_action = QAction("&Export...", self)
        self.export_action.setShortcut(QKeySequence("Ctrl+E"))
        self.exit_action = QAction("E&xit", self)
        self.exit_action.setShortcut(QKeySequence("Alt+F4"))
        self.exit_action.triggered.connect(self.close)

        self.undo_action = QAction("&Undo", self)
        self.undo_action.setShortcut(QKeySequence.Undo)
        self.redo_action = QAction("&Redo", self)
        self.redo_action.setShortcut(QKeySequence.Redo)
        self.find_action = QAction("&Find...", self)
        self.find_action.setShortcut(QKeySequence("Ctrl+F"))

        self.toggle_theme_action = QAction("Toggle &Dark Mode", self)
        self.toggle_theme_action.setShortcut(QKeySequence("Ctrl+T"))
        self.toggle_sidebar_action = QAction("Toggle &Sidebar", self)
        self.toggle_sidebar_action.setShortcut(QKeySequence("Ctrl+B"))

        self.ai_chat_action = QAction("&Chat with AI", self)
        self.ai_chat_action.setShortcut(QKeySequence("Ctrl+Shift+C"))
        self.ai_summarize_action = QAction("&Summarize Note", self)
        self.ai_tag_action = QAction("Auto-&Tag Note", self)
        self.ai_keywords_action = QAction("Extract &Keywords", self)
        self.ai_settings_action = QAction("AI &Settings...", self)

        self.settings_action = QAction("&Settings...", self)
        self.settings_action.setShortcut(QKeySequence("Ctrl+,"))
        self.rebuild_index_action = QAction("Rebuild Search &Index", self)

        self.new_note_action.triggered.connect(self._on_new_note)
        self.new_folder_action.triggered.connect(self._on_new_folder)
        self.rebuild_index_action.triggered.connect(
            lambda: self.search_engine.rebuild_index()
        )
        self.settings_action.triggered.connect(self._open_settings)
        self.ai_settings_action.triggered.connect(self._open_ai_settings)

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.new_note_action)
        file_menu.addAction(self.new_folder_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.find_action)

        view_menu = menu_bar.addMenu("&View")
        view_menu.addAction(self.toggle_theme_action)
        view_menu.addAction(self.toggle_sidebar_action)

        ai_menu = menu_bar.addMenu("&AI")
        ai_menu.addAction(self.ai_chat_action)
        ai_menu.addSeparator()
        ai_menu.addAction(self.ai_summarize_action)
        ai_menu.addAction(self.ai_tag_action)
        ai_menu.addAction(self.ai_keywords_action)
        ai_menu.addSeparator()
        ai_menu.addAction(self.ai_settings_action)

        tools_menu = menu_bar.addMenu("&Tools")
        tools_menu.addAction(self.settings_action)
        tools_menu.addAction(self.rebuild_index_action)

    def _create_toolbar(self):
        toolbar = self.addToolBar("Main")
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setMovable(False)
        toolbar.addAction(self.new_note_action)
        toolbar.addAction(self.new_folder_action)
        toolbar.addSeparator()
        toolbar.addAction(self.find_action)
        toolbar.addSeparator()
        toolbar.addAction(self.ai_chat_action)
        toolbar.addAction(self.toggle_theme_action)

    def _create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.word_count_label = QLabel("Words: 0")
        self.status_bar.addPermanentWidget(self.word_count_label)

    def _create_central_layout(self):
        self.central_splitter = QSplitter(Qt.Orientation.Horizontal)

        self.sidebar = QTabWidget()
        self.sidebar.setMinimumWidth(250)
        self.sidebar.setMaximumWidth(400)

        self.folder_tree = FolderTree(self.folder_service)
        self.note_list = NoteList(self.note_service)
        self.tag_panel = TagPanel(self.tag_service)
        self.search_bar = SearchBar(self.search_service)

        self.sidebar.addTab(self.folder_tree, "Folders")
        self.sidebar.addTab(self.note_list, "Notes")
        self.sidebar.addTab(self.tag_panel, "Tags")
        self.sidebar.addTab(self.search_bar, "Search")

        self.editor_widget = EditorWidget(self.note_service, self.image_service, self.link_service)

        self.right_panel = QTabWidget()
        self.right_panel.setMinimumWidth(250)
        self.right_panel.setMaximumWidth(500)

        self._graph_loaded = False
        self._tree_loaded = False
        self._chat_loaded = False

        placeholder = QLabel("Click to load Graph View")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: palette(placeholder-text);")

        self.right_panel.addTab(placeholder, "Graph")
        self.right_panel.addTab(QLabel("Click to load Tree View"), "Tree")
        self.right_panel.addTab(QLabel("Click to load AI Chat"), "Chat")

        self.right_panel.currentChanged.connect(self._on_right_tab_changed)

        self.central_splitter.addWidget(self.sidebar)
        self.central_splitter.addWidget(self.editor_widget)
        self.central_splitter.addWidget(self.right_panel)
        self.central_splitter.setStretchFactor(0, 1)
        self.central_splitter.setStretchFactor(1, 3)
        self.central_splitter.setStretchFactor(2, 1)

        self.setCentralWidget(self.central_splitter)

    def _post_init(self):
        folder_id = self.folder_tree.get_selected_folder_id()
        if folder_id is not None:
            self.note_list.load_folder(folder_id)
        self._show_status("Welcome to PulsarNote", 5000)

    def _on_right_tab_changed(self, index):
        self.right_panel.blockSignals(True)
        try:
            if index == 0 and not self._graph_loaded:
                from .graph.knowledge_graph_view import KnowledgeGraphWidget
                self.graph_widget = KnowledgeGraphWidget(self.link_service)
                self.right_panel.removeTab(0)
                self.right_panel.insertTab(0, self.graph_widget, "Graph")
                self._graph_loaded = True
            elif index == 1 and not self._tree_loaded:
                from .graph.family_tree_view import FamilyTreeWidget
                self.tree_widget = FamilyTreeWidget(self.topic_service)
                self.right_panel.removeTab(1)
                self.right_panel.insertTab(1, self.tree_widget, "Tree")
                self._tree_loaded = True
            elif index == 2 and not self._chat_loaded:
                from .chat.chat_panel import ChatPanel
                self.chat_panel = ChatPanel(self.ai_config_repo, self.note_service)
                self.right_panel.removeTab(2)
                self.right_panel.insertTab(2, self.chat_panel, "Chat")
                self._chat_loaded = True
        finally:
            self.right_panel.blockSignals(False)

    def _connect_signals(self):
        self._signals.status_message.connect(self._show_status)
        self.note_list.note_selected.connect(self.editor_widget.load_note)
        self.search_bar.search_result_selected.connect(self.editor_widget.load_note)
        self._signals.note_saved.connect(self._update_word_count)
        self._signals.note_selected.connect(self._on_note_selected_for_count)

    def _on_new_note(self):
        folder_id = self.folder_tree.get_selected_folder_id()
        note_id = self.note_service.create("Untitled", folder_id)
        self.note_list.refresh()
        self.editor_widget.load_note(note_id)
        self._signals.status_message.emit("New note created", 3000)

    def _on_new_folder(self):
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and name.strip():
            parent_id = self.folder_tree.get_selected_folder_id()
            self.folder_service.create(name.strip(), parent_id)
            self._signals.folder_changed.emit()
            self._signals.status_message.emit(f'Folder "{name}" created', 3000)

    def _update_word_count(self, note_id: int):
        note = self.note_service.get_by_id(note_id)
        if note:
            self.word_count_label.setText(f"Words: {note.word_count}")

    def _on_note_selected_for_count(self, note_id: int):
        note = self.note_service.get_by_id(note_id)
        if note:
            self.word_count_label.setText(f"Words: {note.word_count}")

    def _show_status(self, message: str, timeout: int = 3000):
        self.status_bar.showMessage(message, timeout)

    def _open_settings(self):
        from .settings.settings_dialog import SettingsDialog
        dlg = SettingsDialog(self)
        dlg.exec()

    def _open_ai_settings(self):
        from .settings.ai_config_panel import AIConfigDialog
        dlg = AIConfigDialog(self.ai_config_repo, self)
        dlg.exec()
