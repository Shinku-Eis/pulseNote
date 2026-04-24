"""Business logic for notes."""
from ..core.models import Note
from ..core.repository import NoteRepository


class NoteService:
    def __init__(self, note_repo: NoteRepository):
        self._repo = note_repo

    def get_all(self):
        return self._repo.get_all()

    def get_by_folder(self, folder_id: int | None):
        return self._repo.get_by_folder(folder_id)

    def get_by_id(self, note_id: int) -> Note | None:
        return self._repo.get_by_id(note_id)

    def create(self, title: str, folder_id: int | None = None) -> int:
        note = Note(title=title, folder_id=folder_id, content="", word_count=0)
        return self._repo.create(note)

    def update(self, note: Note):
        note.word_count = len(note.content.split())
        self._repo.update(note)

    def delete(self, note_id: int):
        self._repo.delete(note_id)
