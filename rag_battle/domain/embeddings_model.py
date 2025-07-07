from abc import ABC, abstractmethod


class BaseEmbeddingsModel(ABC):
    @abstractmethod
    async def embed_queries(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    @abstractmethod
    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError
