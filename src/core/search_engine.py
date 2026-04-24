"""Simple FTS search engine using SQLite FTS5."""
import sqlite3


class SearchEngine:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._init_fts()

    def _init_fts(self):
        self._conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts
            USING fts5(title, content, content_rowid, tokenize='porter')
        """)
        self._conn.commit()

    def rebuild_index(self):
        self._conn.execute("DELETE FROM notes_fts")
        self._conn.execute("""
            INSERT INTO notes_fts (rowid, title, content)
            SELECT id, title, content FROM notes
        """)
        self._conn.commit()

    def search(self, query: str, limit: int = 50) -> list[dict]:
        if not query.strip():
            return []
        rows = self._conn.execute("""
            SELECT n.id, n.title, n.updated_at, snippet(notes_fts, 1, '[', ']', '...', 30) as preview
            FROM notes_fts f
            JOIN notes n ON f.rowid = n.id
            WHERE notes_fts MATCH ?
            ORDER BY bm25(notes_fts)
            LIMIT ?
        """, (query, limit)).fetchall()
        return [dict(r) for r in rows]

    def update_index(self, note_id: int, title: str, content: str):
        self._conn.execute("DELETE FROM notes_fts WHERE rowid=?", (note_id,))
        self._conn.execute(
            "INSERT INTO notes_fts (rowid, title, content) VALUES (?, ?, ?)",
            (note_id, title, content)
        )
        self._conn.commit()

    def remove_from_index(self, note_id: int):
        self._conn.execute("DELETE FROM notes_fts WHERE rowid=?", (note_id,))
        self._conn.commit()
