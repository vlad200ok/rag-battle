from abc import ABC, abstractmethod


class BaseEmbeddingsModel(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError
