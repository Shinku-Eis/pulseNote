"""Business logic for images."""
from ..core.models import Image
from ..core.repository import ImageRepository


class ImageService:
    def __init__(self, image_repo: ImageRepository):
        self._repo = image_repo

    def get_by_id(self, image_id: int):
        return self._repo.get_by_id(image_id)

    def get_by_note(self, note_id: int):
        return self._repo.get_by_note(note_id)

    def create(self, note_id: int, filename: str, data: bytes, mime_type: str = "image/png") -> int:
        img = Image(note_id=note_id, filename=filename, data=data, mime_type=mime_type)
        return self._repo.create(img)

    def delete(self, image_id: int):
        self._repo.delete(image_id)
