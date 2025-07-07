import numpy as np
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any
from dataclasses import dataclass


@dataclass
class DataItem:
    item_id: str
    content: Any
    tags: list[str]
    score: float | None = None


@dataclass
class DataItemWithEmbedding:
    item: DataItem
    embedding: np.ndarray


DataItemType = TypeVar("DataItemType", bound=DataItem)
DataItemWithEmbeddingType = TypeVar(
    "DataItemWithEmbeddingType", bound=DataItemWithEmbedding
)


class VectorDatabase(Generic[DataItemType], ABC):
    @abstractmethod
    async def save_items(
        self,
        items_with_embeddings: list[DataItemWithEmbeddingType],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def query(
        self,
        query_embeddings: list[np.ndarray],
        tags: list[str],
        num_items: int,
        remove_duplicates: bool,
    ) -> list[DataItemType]:
        raise NotImplementedError
