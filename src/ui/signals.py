"""Centralized signals for cross-module communication."""
from PyQt6.QtCore import QObject, pyqtSignal


class Signals(QObject):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    note_selected = pyqtSignal(int)
    note_saved = pyqtSignal(int)
    note_created = pyqtSignal(int)
    note_deleted = pyqtSignal(int)
    note_list_refresh = pyqtSignal()

    folder_selected = pyqtSignal(object)
    folder_changed = pyqtSignal()

    search_requested = pyqtSignal(str)

    tag_changed = pyqtSignal()

    topic_selected = pyqtSignal(int)
    topic_changed = pyqtSignal()
    topic_focus_requested = pyqtSignal(int)

    ai_processing_started = pyqtSignal()
    ai_processing_finished = pyqtSignal()
    ai_config_changed = pyqtSignal()

    status_message = pyqtSignal(str, int)


signals = Signals()
