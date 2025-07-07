import numpy as np
from typing import TypeVar
from dataclasses import dataclass


@dataclass
class RAGQuery:
    query: str
    tags: list[str]
    num_items: int
    remove_duplicates: bool = True


@dataclass
class DataItem:
    item_id: str
    content: str
    tags: list[str]
    score: float | None = None


# TODO: move to schemas
@dataclass
class DataItemWithEmbedding:
    item: DataItem
    embedding: np.ndarray


DataItemType = TypeVar("DataItemType", bound=DataItem)
DataItemWithEmbeddingType = TypeVar(
    "DataItemWithEmbeddingType", bound=DataItemWithEmbedding
)
