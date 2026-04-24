"""Business logic for tags."""
from ..core.models import Tag
from ..core.repository import TagRepository, NoteRepository


class TagService:
    def __init__(self, tag_repo: TagRepository, note_repo: NoteRepository):
        self._tag_repo = tag_repo
        self._note_repo = note_repo

    def get_all(self) -> list[Tag]:
        return self._tag_repo.get_all()

    def get_by_id(self, tag_id: int) -> Tag | None:
        return self._tag_repo.get_by_id(tag_id)

    def create(self, name: str, color: str | None = None) -> int:
        tag = Tag(name=name, color=color)
        return self._tag_repo.create(tag)

    def update(self, tag: Tag):
        self._tag_repo.update(tag)

    def delete(self, tag_id: int):
        self._tag_repo.delete(tag_id)
