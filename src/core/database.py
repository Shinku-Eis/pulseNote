"""SQLite database connection and initialization."""
import sqlite3
import os
from ..utils.resource_path import resource_path


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        db_path = os.path.join(os.path.expanduser("~"), ".pulsarnote", "notes.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

        schema_path = resource_path(os.path.join("src", "core", "schema.sql"))
        with open(schema_path, "r", encoding="utf-8") as f:
            self.conn.executescript(f.read())
        self.conn.commit()

    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close()
