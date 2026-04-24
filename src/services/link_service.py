"""Business logic for note links."""
from ..core.models import NoteLink
from ..core.repository import NoteLinkRepository, NoteRepository


class LinkService:
    def __init__(self, link_repo: NoteLinkRepository, note_repo: NoteRepository):
        self._link_repo = link_repo
        self._note_repo = note_repo

    def get_all(self):
        return self._link_repo.get_all()

    def get_by_note(self, note_id: int):
        return self._link_repo.get_by_note(note_id)

    def create(self, from_note_id: int, to_note_id: int, relation_type: str = "link"):
        link = NoteLink(from_note_id=from_note_id, to_note_id=to_note_id, relation_type=relation_type)
        return self._link_repo.create(link)

    def delete(self, link_id: int):
        self._link_repo.delete(link_id)
