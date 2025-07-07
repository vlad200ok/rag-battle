import numpy as np
from abc import ABC, abstractmethod
from typing import Generic
from rag_battle.domain.schemas import DataItemType, DataItemWithEmbeddingType


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
