from abc import ABC, abstractmethod
from rag_battle.infra.embeddings.base import BaseEmbeddingsModel


class BaseRetriever(ABC):
    def __init__(self, embeddings_model: BaseEmbeddingsModel):
        self._embeddings_model = embeddings_model

    @abstractmethod
    async def retrieve(self, query: str) -> list[str]:
        raise NotImplementedError
