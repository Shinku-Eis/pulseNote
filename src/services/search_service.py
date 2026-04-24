"""Search service."""
from ..core.search_engine import SearchEngine


class SearchService:
    def __init__(self, search_engine: SearchEngine):
        self._engine = search_engine

    def search(self, query: str, limit: int = 50):
        return self._engine.search(query, limit)

    def rebuild_index(self):
        self._engine.rebuild_index()

    def update_index(self, note_id: int, title: str, content: str):
        self._engine.update_index(note_id, title, content)

    def remove_from_index(self, note_id: int):
        self._engine.remove_from_index(note_id)
