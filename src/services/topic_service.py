"""Business logic for knowledge topics."""
from ..core.models import KnowledgeTopic, TopicConnection
from ..core.repository import KnowledgeTopicRepository, TopicConnectionRepository


class TopicService:
    def __init__(self, topic_repo: KnowledgeTopicRepository, conn_repo: TopicConnectionRepository):
        self._topic_repo = topic_repo
        self._conn_repo = conn_repo

    def get_all(self):
        return self._topic_repo.get_all()

    def get_by_id(self, topic_id: int):
        return self._topic_repo.get_by_id(topic_id)

    def create(self, name: str, description: str = ""):
        topic = KnowledgeTopic(name=name, description=description)
        return self._topic_repo.create(topic)

    def update(self, topic: KnowledgeTopic):
        self._topic_repo.update(topic)

    def delete(self, topic_id: int):
        self._topic_repo.delete(topic_id)

    def get_all_connections(self):
        return self._conn_repo.get_all()
