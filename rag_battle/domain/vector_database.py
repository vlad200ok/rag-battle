import numpy as np
from abc import ABC, abstractmethod
from typing import Generic
from rag_battle.domain.schemas import DataItemType, DataItemWithEmbeddingType


class VectorDatabase(Generic[DataItemType], ABC):
    """
    Abstract base class for vector database implementations.

    Vector databases store document embeddings and enable efficient similarity search.
    This interface allows for different database backends to be used in the RAG system,
    such as FAISS, Milvus, Qdrant, or custom implementations.

    Type Parameters:
        DataItemType: The specific type of data item stored in the database.
    """

    @abstractmethod
    async def save_items(
        self,
        items_with_embeddings: list[DataItemWithEmbeddingType],
    ) -> None:
        """
        Save multiple items with their embeddings to the vector database.

        :param items_with_embeddings: List of data items with their corresponding
        vector embeddings to be stored.
        """
        raise NotImplementedError

    @abstractmethod
    async def query(
        self,
        query_embeddings: list[np.ndarray],
        tags: list[str],
        num_items: int,
        remove_duplicates: bool,
    ) -> list[DataItemType]:
        """
        Query the vector database for items similar to the provided embeddings.

        :param query_embeddings: The vector representations of the query.
        :param tags: Tags to filter documents by.
        :param num_items: Maximum number of items to return.
        :param remove_duplicates: Whether to remove duplicate results.

        :return: list[DataItemType]: A list of retrieved items ordered by similarity.

        """
        raise NotImplementedError
