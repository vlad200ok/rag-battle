from abc import ABC, abstractmethod
from rag_battle.domain.schemas import RAGQuery
from rag_battle.domain.embeddings_model import BaseEmbeddingsModel
from rag_battle.domain.vector_database import VectorDatabase, DataItemType


class BaseRetriever(ABC):
    def __init__(
        self,
        embeddings_model: BaseEmbeddingsModel,
        vector_database: VectorDatabase,
    ):
        self._embeddings_model = embeddings_model
        self._vector_database = vector_database

    @abstractmethod
    async def retrieve(self, query: RAGQuery) -> list[DataItemType]:
        raise NotImplementedError
