"""Domain models - simple dataclasses."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Folder:
    name: str
    parent_id: Optional[int] = None
    sort_order: int = 0
    icon: Optional[str] = None
    color: Optional[str] = None
    id: Optional[int] = None


@dataclass
class Note:
    title: str
    content: str = ""
    folder_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    word_count: int = 0
    id: Optional[int] = None


@dataclass
class Tag:
    name: str
    color: Optional[str] = None
    id: Optional[int] = None


@dataclass
class NoteLink:
    from_note_id: int
    to_note_id: int
    relation_type: str = "link"
    id: Optional[int] = None


@dataclass
class KnowledgeTopic:
    name: str
    description: str = ""
    color: Optional[str] = None
    parent_id: Optional[int] = None
    id: Optional[int] = None


@dataclass
class TopicConnection:
    from_topic_id: int
    to_topic_id: int
    strength: float = 1.0
    id: Optional[int] = None


@dataclass
class AIConfig:
    provider: str = "openai"
    model: str = "gpt-3.5-turbo"
    api_key: str = ""
    api_base: str = ""
    temperature: float = 0.7
    max_tokens: int = 2000
    id: Optional[int] = None


@dataclass
class Image:
    note_id: int
    filename: str
    data: bytes
    mime_type: str = "image/png"
    id: Optional[int] = None


@dataclass
class NoteListItem:
    id: int
    title: str
    preview: str
    updated_at: str
    folder_id: Optional[int] = None
