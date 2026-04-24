-- PulsarNote database schema

CREATE TABLE IF NOT EXISTS folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    sort_order INTEGER DEFAULT 0,
    icon TEXT,
    color TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES folders(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT DEFAULT '',
    folder_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    word_count INTEGER DEFAULT 0,
    FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    color TEXT
);

CREATE TABLE IF NOT EXISTS note_tags (
    note_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (note_id, tag_id),
    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS note_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_note_id INTEGER NOT NULL,
    to_note_id INTEGER NOT NULL,
    relation_type TEXT DEFAULT 'link',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_note_id) REFERENCES notes(id) ON DELETE CASCADE,
    FOREIGN KEY (to_note_id) REFERENCES notes(id) ON DELETE CASCADE,
    UNIQUE(from_note_id, to_note_id)
);

CREATE TABLE IF NOT EXISTS knowledge_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    color TEXT,
    parent_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES knowledge_topics(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS topic_connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_topic_id INTEGER NOT NULL,
    to_topic_id INTEGER NOT NULL,
    strength REAL DEFAULT 1.0,
    FOREIGN KEY (from_topic_id) REFERENCES knowledge_topics(id) ON DELETE CASCADE,
    FOREIGN KEY (to_topic_id) REFERENCES knowledge_topics(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS note_topics (
    note_id INTEGER,
    topic_id INTEGER,
    PRIMARY KEY (note_id, topic_id),
    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES knowledge_topics(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ai_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT DEFAULT 'openai',
    model TEXT DEFAULT 'gpt-3.5-turbo',
    api_key TEXT DEFAULT '',
    api_base TEXT DEFAULT '',
    temperature REAL DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 2000
);

CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id INTEGER,
    filename TEXT NOT NULL,
    data BLOB NOT NULL,
    mime_type TEXT DEFAULT 'image/png',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS ai_processing_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id INTEGER,
    action TEXT NOT NULL,
    status TEXT NOT NULL,
    result TEXT,
    error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_notes_folder ON notes(folder_id);
CREATE INDEX IF NOT EXISTS idx_notes_updated ON notes(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_note_links_from ON note_links(from_note_id);
CREATE INDEX IF NOT EXISTS idx_note_links_to ON note_links(to_note_id);

INSERT OR IGNORE INTO folders (id, name, parent_id) VALUES (1, 'Default', NULL);
INSERT OR IGNORE INTO ai_configs (id) VALUES (1);
