"""Business logic for folders."""
from ..core.models import Folder
from ..core.repository import FolderRepository


class FolderService:
    def __init__(self, folder_repo: FolderRepository):
        self._repo = folder_repo

    def get_all(self) -> list[Folder]:
        return self._repo.get_all()

    def get_children(self, parent_id: int | None) -> list[Folder]:
        return self._repo.get_children(parent_id)

    def get_by_id(self, folder_id: int) -> Folder | None:
        return self._repo.get_by_id(folder_id)

    def create(self, name: str, parent_id: int | None = None) -> int:
        siblings = self.get_children(parent_id)
        sort_order = len(siblings)
        folder = Folder(name=name, parent_id=parent_id, sort_order=sort_order)
        return self._repo.create(folder)

    def update(self, folder: Folder):
        self._repo.update(folder)

    def delete(self, folder_id: int):
        self._repo.delete(folder_id)

    def build_tree(self) -> list[dict]:
        all_folders = self.get_all()
        folder_map = {f.id: {"folder": f, "children": []} for f in all_folders}
        roots = []
        for f in all_folders:
            if f.parent_id is None:
                roots.append(folder_map[f.id])
            else:
                if f.parent_id in folder_map:
                    folder_map[f.parent_id]["children"].append(folder_map[f.id])
        return roots
