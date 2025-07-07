from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pydantic import BaseModel, ConfigDict


class EmbeddingsModelConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    model_name: str
    embedding_size: int


EmbeddingsModelConfigType = TypeVar(
    "EmbeddingsModelConfigType", bound=EmbeddingsModelConfig
)


class BaseEmbeddingsModel(Generic[EmbeddingsModelConfigType], ABC):
    def __init__(self, config: EmbeddingsModelConfigType):
        self._config = config

    @abstractmethod
    async def embed_queries(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    @abstractmethod
    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError
