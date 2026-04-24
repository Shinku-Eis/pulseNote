"""Repository classes for all entities."""
from __future__ import annotations
import sqlite3
from typing import Optional
from .models import (
    Folder, Note, Tag, NoteLink, KnowledgeTopic,
    TopicConnection, AIConfig, Image, NoteListItem
)


class FolderRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_all(self) -> list[Folder]:
        rows = self._conn.execute(
            "SELECT * FROM folders ORDER BY sort_order, name"
        ).fetchall()
        return [Folder(**dict(r)) for r in rows]

    def get_children(self, parent_id: int | None) -> list[Folder]:
        if parent_id is None:
            rows = self._conn.execute(
                "SELECT * FROM folders WHERE parent_id IS NULL ORDER BY sort_order, name"
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM folders WHERE parent_id=? ORDER BY sort_order, name",
                (parent_id,)
            ).fetchall()
        return [Folder(**dict(r)) for r in rows]

    def get_by_id(self, folder_id: int) -> Folder | None:
        row = self._conn.execute("SELECT * FROM folders WHERE id=?", (folder_id,)).fetchone()
        return Folder(**dict(row)) if row else None

    def create(self, folder: Folder) -> int:
        cur = self._conn.execute(
            """INSERT INTO folders (name, parent_id, sort_order, icon, color)
               VALUES (?, ?, ?, ?, ?)""",
            (folder.name, folder.parent_id, folder.sort_order, folder.icon, folder.color)
        )
        self._conn.commit()
        return cur.lastrowid

    def update(self, folder: Folder):
        self._conn.execute(
            """UPDATE folders SET name=?, parent_id=?, sort_order=?, icon=?, color=?
               WHERE id=?""",
            (folder.name, folder.parent_id, folder.sort_order, folder.icon, folder.color, folder.id)
        )
        self._conn.commit()

    def delete(self, folder_id: int):
        self._conn.execute("DELETE FROM folders WHERE id=?", (folder_id,))
        self._conn.commit()


class NoteRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_all(self) -> list[NoteListItem]:
        rows = self._conn.execute(
            """SELECT id, title, substr(content, 1, 200) as preview, updated_at, folder_id
               FROM notes ORDER BY updated_at DESC"""
        ).fetchall()
        return [NoteListItem(**dict(r)) for r in rows]

    def get_by_folder(self, folder_id: int | None) -> list[NoteListItem]:
        if folder_id is None:
            return self.get_all()
        rows = self._conn.execute(
            """SELECT id, title, substr(content, 1, 200) as preview, updated_at, folder_id
               FROM notes WHERE folder_id=? ORDER BY updated_at DESC""",
            (folder_id,)
        ).fetchall()
        return [NoteListItem(**dict(r)) for r in rows]

    def get_by_id(self, note_id: int) -> Note | None:
        row = self._conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
        return Note(**dict(row)) if row else None

    def create(self, note: Note) -> int:
        cur = self._conn.execute(
            """INSERT INTO notes (title, content, folder_id, word_count)
               VALUES (?, ?, ?, ?)""",
            (note.title, note.content, note.folder_id, note.word_count)
        )
        self._conn.commit()
        return cur.lastrowid

    def update(self, note: Note):
        self._conn.execute(
            """UPDATE notes SET title=?, content=?, folder_id=?, word_count=?,
               updated_at=CURRENT_TIMESTAMP WHERE id=?""",
            (note.title, note.content, note.folder_id, note.word_count, note.id)
        )
        self._conn.commit()

    def delete(self, note_id: int):
        self._conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
        self._conn.commit()


class TagRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_all(self) -> list[Tag]:
        rows = self._conn.execute("SELECT * FROM tags ORDER BY name").fetchall()
        return [Tag(**dict(r)) for r in rows]

    def get_by_id(self, tag_id: int) -> Tag | None:
        row = self._conn.execute("SELECT * FROM tags WHERE id=?", (tag_id,)).fetchone()
        return Tag(**dict(row)) if row else None

    def create(self, tag: Tag) -> int:
        cur = self._conn.execute(
            "INSERT OR IGNORE INTO tags (name, color) VALUES (?, ?)",
            (tag.name, tag.color)
        )
        self._conn.commit()
        if cur.lastrowid == 0:
            row = self._conn.execute("SELECT id FROM tags WHERE name=?", (tag.name,)).fetchone()
            return row[0]
        return cur.lastrowid

    def update(self, tag: Tag):
        self._conn.execute(
            "UPDATE tags SET name=?, color=? WHERE id=?",
            (tag.name, tag.color, tag.id)
        )
        self._conn.commit()

    def delete(self, tag_id: int):
        self._conn.execute("DELETE FROM tags WHERE id=?", (tag_id,))
        self._conn.commit()


class NoteLinkRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_all(self) -> list[NoteLink]:
        rows = self._conn.execute("SELECT * FROM note_links").fetchall()
        return [NoteLink(**dict(r)) for r in rows]

    def get_by_note(self, note_id: int) -> list[NoteLink]:
        rows = self._conn.execute(
            "SELECT * FROM note_links WHERE from_note_id=? OR to_note_id=?",
            (note_id, note_id)
        ).fetchall()
        return [NoteLink(**dict(r)) for r in rows]

    def create(self, link: NoteLink) -> int:
        cur = self._conn.execute(
            """INSERT OR IGNORE INTO note_links (from_note_id, to_note_id, relation_type)
               VALUES (?, ?, ?)""",
            (link.from_note_id, link.to_note_id, link.relation_type)
        )
        self._conn.commit()
        return cur.lastrowid

    def delete(self, link_id: int):
        self._conn.execute("DELETE FROM note_links WHERE id=?", (link_id,))
        self._conn.commit()


class KnowledgeTopicRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_all(self) -> list[KnowledgeTopic]:
        rows = self._conn.execute("SELECT * FROM knowledge_topics ORDER BY name").fetchall()
        return [KnowledgeTopic(**dict(r)) for r in rows]

    def get_by_id(self, topic_id: int) -> KnowledgeTopic | None:
        row = self._conn.execute("SELECT * FROM knowledge_topics WHERE id=?", (topic_id,)).fetchone()
        return KnowledgeTopic(**dict(row)) if row else None

    def create(self, topic: KnowledgeTopic) -> int:
        cur = self._conn.execute(
            """INSERT INTO knowledge_topics (name, description, color, parent_id)
               VALUES (?, ?, ?, ?)""",
            (topic.name, topic.description, topic.color, topic.parent_id)
        )
        self._conn.commit()
        return cur.lastrowid

    def update(self, topic: KnowledgeTopic):
        self._conn.execute(
            """UPDATE knowledge_topics SET name=?, description=?, color=?, parent_id=?
               WHERE id=?""",
            (topic.name, topic.description, topic.color, topic.parent_id, topic.id)
        )
        self._conn.commit()

    def delete(self, topic_id: int):
        self._conn.execute("DELETE FROM knowledge_topics WHERE id=?", (topic_id,))
        self._conn.commit()


class TopicConnectionRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_all(self) -> list[TopicConnection]:
        rows = self._conn.execute("SELECT * FROM topic_connections").fetchall()
        return [TopicConnection(**dict(r)) for r in rows]

    def create(self, conn: TopicConnection) -> int:
        cur = self._conn.execute(
            """INSERT INTO topic_connections (from_topic_id, to_topic_id, strength)
               VALUES (?, ?, ?)""",
            (conn.from_topic_id, conn.to_topic_id, conn.strength)
        )
        self._conn.commit()
        return cur.lastrowid


class AIConfigRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get(self) -> AIConfig:
        row = self._conn.execute("SELECT * FROM ai_configs WHERE id=1").fetchone()
        if not row:
            self._conn.execute("INSERT INTO ai_configs (id) VALUES (1)")
            self._conn.commit()
            return AIConfig(id=1)
        return AIConfig(**dict(row))

    def update(self, config: AIConfig):
        self._conn.execute(
            """UPDATE ai_configs SET provider=?, model=?, api_key=?, api_base=?,
               temperature=?, max_tokens=? WHERE id=1""",
            (config.provider, config.model, config.api_key, config.api_base,
             config.temperature, config.max_tokens)
        )
        self._conn.commit()


class ImageRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get_by_id(self, image_id: int) -> Image | None:
        row = self._conn.execute("SELECT * FROM images WHERE id=?", (image_id,)).fetchone()
        return Image(**dict(row)) if row else None

    def get_by_note(self, note_id: int) -> list[Image]:
        rows = self._conn.execute("SELECT * FROM images WHERE note_id=?", (note_id,)).fetchall()
        return [Image(**dict(r)) for r in rows]

    def create(self, image: Image) -> int:
        cur = self._conn.execute(
            """INSERT INTO images (note_id, filename, data, mime_type)
               VALUES (?, ?, ?, ?)""",
            (image.note_id, image.filename, image.data, image.mime_type)
        )
        self._conn.commit()
        return cur.lastrowid

    def delete(self, image_id: int):
        self._conn.execute("DELETE FROM images WHERE id=?", (image_id,))
        self._conn.commit()


class SettingsRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def get(self, key: str, default=None):
        row = self._conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row[0] if row else default

    def set(self, key: str, value: str):
        self._conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value)
        )
        self._conn.commit()


class AIProcessingLogRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def create(self, note_id: int, action: str, status: str, result=None, error=None):
        self._conn.execute(
            """INSERT INTO ai_processing_logs (note_id, action, status, result, error)
               VALUES (?, ?, ?, ?, ?)""",
            (note_id, action, status, result, error)
        )
        self._conn.commit()
