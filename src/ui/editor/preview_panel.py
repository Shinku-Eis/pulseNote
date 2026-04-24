"""HTML preview panel for markdown rendering."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage

from ...utils.markdown_renderer import render_markdown


class PreviewPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._web = QWebEngineView()
        self._web.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self._web.page().setBackgroundColor(Qt.GlobalColor.black)

        layout.addWidget(self._web)

    def render(self, content: str):
        html = render_markdown(content)
        self._web.setHtml(html)
