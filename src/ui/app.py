"""QApplication subclass with theme support."""
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ..utils.resource_path import resource_path


class PulsarApp(QApplication):

    def __init__(self, argv: list):
        super().__init__(argv)
        self.setApplicationName("PulsarNote")
        self.setApplicationDisplayName("PulsarNote")
        self._dark_mode = False
        self._load_theme()

    def _load_theme(self):
        style_dir = resource_path(os.path.join("resources", "styles"))
        theme_file = os.path.join(style_dir, "dark_theme.qss" if self._dark_mode else "light_theme.qss")
        if os.path.exists(theme_file):
            with open(theme_file, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def toggle_theme(self):
        self._dark_mode = not self._dark_mode
        self._load_theme()

    @property
    def is_dark_mode(self) -> bool:
        return self._dark_mode
