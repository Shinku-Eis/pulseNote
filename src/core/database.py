"""SQLite database connection and initialization.
FIXED: Database location moved to local app folder (not user home folder)
to avoid permission errors in sandbox/protected environments.
"""
import sqlite3
import os
import sys
from ..utils.resource_path import resource_path


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        # Use local folder where EXE is running, NOT user home
        # This avoids permission errors in sandbox environments
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.getcwd()

        db_dir = os.path.join(base_dir, "data")
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "notes.db")

        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

        schema_path = resource_path(os.path.join("src", "core", "schema.sql"))
        with open(schema_path, "r", encoding="utf-8") as f:
            self.conn.executescript(f.read())
        self.conn.commit()

    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close()
