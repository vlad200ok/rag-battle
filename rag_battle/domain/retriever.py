from abc import ABC, abstractmethod
from rag_battle.domain.embeddings_model import BaseEmbeddingsModel


class BaseRetriever(ABC):
    def __init__(self, embeddings_model: BaseEmbeddingsModel):
        self._embeddings_model = embeddings_model

    @abstractmethod
    async def retrieve(self, query: str) -> list[str]:
        raise NotImplementedError
